import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from payment import models
from api.v1.payment.mixins import AlifSignatureAuthMixin
from api.v1.payment.services.transaction import TransactionManager
from api.v1.payment.services.integrations.uzum_gateway import UzumPaymentGateway
from api.v1.payment.services.integrations.alif_gateway import AlifPaymentGateway


# Uzum
class GenerateUzumLinkView(APIView):

    def get(self, request, *args, **kwargs):
        # TODO get user, get order data -> set at creation
        amount = 2500000
        order = models.Order.objects.create(owner_id=1)
        base_url = "https://apelsin.uz/ecom-qr"
        TransactionManager.create_instance(data={
            "order": order,
            "payment_service": models.Transaction.PaymentServiceChoices.alif,
            "amount": amount,
        })
        link = f"{base_url}?serviceId={settings.UZUM_SERVICE_ID}&orderId={order.pk}&amount={amount}"
        return Response({"link": link})


class UzumCheckAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return UzumPaymentGateway.process_check(request.data)


class UzumCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return UzumPaymentGateway.process_create(request.data)


class UzumConfirmAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return UzumPaymentGateway.process_confirm(request.data)


class UzumReverseAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return UzumPaymentGateway.process_reverse(request.data)


class UzumStatusAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return UzumPaymentGateway.process_status(request.data)


# Alif
class GenerateAlifLinkView(APIView):

    def get(self, request, *args, **kwargs):
        # TODO get user, get order data -> set at creation
        order = models.Order.objects.create(owner_id=1)
        transaction = TransactionManager.create_instance(data={
            "order": order,
            "payment_service": models.Transaction.PaymentServiceChoices.alif,
            "amount": 2500000,
        })
        item_name = "Subscription purchase"
        headers = {"Token": settings.ALIF_TOKEN}
        cancel_url = ""
        redirect_url = ""
        webhook_url = f"{request.scheme}://{request.get_host()}/ru/api/v1/payment/alif-merchant/webhook"
        data = {
            "items": [
                {
                    "name": item_name,
                    "amount": 1,
                    "price":  transaction.amount,
                    "discount": 0,
                    "vat_percent": 0,
                    "spic": "10302001005000000",
                }
            ],
            "receipt": True,
            "cancel_url": cancel_url,
            "redirect_url": redirect_url,
            "webhook_url": webhook_url,
            "timeout": 86400,
        }
        response = requests.post(
            url=f"{settings.ALIF_BASE_URL}/invoice",
            headers=headers,
            json=data,
        )
        link = None
        if response.status_code == 200:
            link = f"https://checkout-dev.alifpay.uz/?invoice={response.json().get('id')}",
            TransactionManager.update_instance(
                instance=transaction,
                data={"transaction_id": response.json().get("id")}
            )
        return Response({"link": link})


class AlifGetInvoiceAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return AlifPaymentGateway.get_invoice(request)


class AlifRefundInvoiceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return AlifPaymentGateway.refund_invoice(request)


class AlifSendInvoiceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return AlifPaymentGateway.send_invoice(request)


class AlifWebhookAPIView(APIView):

    def post(self, request, *args, **kwargs):
        return AlifPaymentGateway.webhook(request)

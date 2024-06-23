import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from payment import models


class AlifPaymentGateway:

    @staticmethod
    def get_invoice(request):
        transaction = get_object_or_404(
            models.Transaction,
            pk=request.data.get("pk"),
            order__user_id=request._auth.payload["user_id"],
        )
        url = f"{settings.ALIF_BASE_URL}/getInvoice"
        response = requests.post(
            url=url,
            data={"id": transaction.transaction_id},
            headers={"Authorization": settings.ALIF_TOKEN},
        )
        if response.status_code == 200:
            return JsonResponse(
                {"status": response.json()["payment"]["status"]},
                status=200
            )
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def refund_invoice(request):
        transaction = get_object_or_404(
            models.Transaction,
            pk=request.data.get("pk"),
            order__user_id=request._auth.payload["user_id"],
        )
        url = f"{settings.ALIF_BASE_URL}/refundInvoice"
        response = requests.post(
            url=url,
            data={"id": transaction.transaction_id},
            headers={"Authorization": settings.ALIF_TOKEN},
        )
        if response.status_code == 200:
            status = response.json()["payment"]["status"]
            if status == "REVERTED":
                # TODO
                pass
            return JsonResponse({"status": status},status=200)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def send_invoice(request):
        return JsonResponse({}, status=200)

    @staticmethod
    def webhook(request):
        transaction_id = request.data["id"]
        status = request.data["payment"]["status"]
        transaction = get_object_or_404(
            models.Transaction,
            transaction_id=transaction_id,
            order__user_id=request._auth.payload["user_id"],
        )
        return JsonResponse({}, status=200)

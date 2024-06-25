import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from payment import models


class AlifPaymentGateway:

    @staticmethod
    def get_invoice(request):
        user_id = 1 # request._auth.payload.get("user_id")
        transaction = get_object_or_404(
            models.Transaction,
            pk=request.data.get("pk"),
            order__owner_id=user_id,
        )
        url = f"{settings.ALIF_BASE_URL}/getInvoice"
        response = requests.post(
            url=url,
            json={"id": transaction.transaction_id},
            headers={"Token": settings.ALIF_TOKEN},
        )
        if response.status_code == 200:
            return JsonResponse(
                {"status": response.json()["payment"].get("status")},
                status=200
            )
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def refund_invoice(request):
        user_id = 1 # request._auth.payload["user_id"]
        transaction = get_object_or_404(
            models.Transaction,
            pk=request.data.get("pk"),
            order__user_id=user_id,
        )
        url = f"{settings.ALIF_BASE_URL}/refundInvoice"
        response = requests.post(
            url=url,
            json={"id": transaction.transaction_id},
            headers={"Token": settings.ALIF_TOKEN},
        )
        if response.status_code == 200:
            status = response.json()["payment"].get("status")
            if status == "REVERTED":
                transaction.status = models.Transaction.StatusChoices.canceled
                transaction.save()
            return JsonResponse({"status": status}, status=200)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def send_invoice(request):
        user_id = 1 # request._auth.payload["user_id"]
        transaction = get_object_or_404(
            models.Transaction,
            pk=request.data.get("pk"),
            order__user_id=user_id,
        )
        phone_number = request.data.get("phone")
        url = f"{settings.ALIF_BASE_URL}/sendInvoice"
        response = requests.post(
            url=url,
            json={"id": transaction.transaction_id, "phone": phone_number},
            headers={"Token": settings.ALIF_TOKEN},
        )
        if response.status_code:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def webhook(request):
        # TODO
        user_id = 1 # request._auth.payload["user_id"]
        transaction_id = request.data["id"]
        status = request.data["payment"]["status"]
        transaction = get_object_or_404(
            models.Transaction,
            transaction_id=transaction_id,
            order__owner_id=user_id,
        )
        if status == "SUCCEEDED":
            transaction.status = models.Transaction.StatusChoices.paid
            transaction.additional_parameters["payload"] = request.data["payment"]["payload"]
        elif status == "REVERTED":
            transaction.status = models.Transaction.StatusChoices.canceled
            transaction.additional_parameters["payload"] = request.data["payment"]["payload"]
        transaction.save()
        return JsonResponse({}, status=200)

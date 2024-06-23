import time
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from api.v1.payment.services.transaction import TransactionManager
from payment import models


def service_id_valid(service_id):
    return service_id == settings.UZUM_SERVICE_ID


class UzumPaymentGateway:

    @staticmethod
    def process_check(data):
        service_id = data.get("serviceId")
        timestamp = data.get("timestamp")
        params = data.get("params")
        #
        if not service_id_valid(service_id):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10006}, status=400
            )
        if not isinstance(params, dict) or not isinstance(timestamp, int):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10002}, status=400
            )
        #
        order_id = params.get("order_id")
        try:
            order = models.Order.objects.get(pk=order_id, is_paid=False)
            if not order.transactions.all().exists():
                return JsonResponse(
                    {"status": "FAILED", "errorCode": 99999}, status=400
                )
        except models.Order.DoesNotExist:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10007}, status=400
            )
        #
        return JsonResponse(
            {
                "serviceId": service_id,
                "timestamp": round(time.time() * 1000),
                "status": "OK",
                "data": {"order_id": order_id}
            },
            status=200
        )

    @staticmethod
    def process_create(data):
        service_id = data.get("serviceId")
        timestamp = data.get("timestamp")
        trans_id = data.get("transId")
        params = data.get("params")
        amount = data.get("amount")
        #
        if not service_id_valid(service_id):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10006}, status=400
            )
        if (
            not isinstance(params, dict) or
            not isinstance(timestamp, int) or
            not isinstance(trans_id, str)
        ):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10002}, status=400
            )
        #
        order_id = params.get("order_id")
        try:
            order = models.Order.objects.get(pk=order_id, is_paid=False)
        except models.Order.DoesNotExist:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10007}, status=400
            )
        #
        if models.Transaction.objects.filter(transaction_id=trans_id).exists():
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10010}, status=400
            )
        #
        transaction = models.Transaction.objects.filter(order=order).order_by(
            "-created_at"
        ).first()
        if not transaction:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 99999}, status=400
            )
        if transaction.amount != amount:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10011}, status=400
            )
        #
        TransactionManager.update_instance(
            transaction, {"transaction": trans_id, "created_at": timezone.now()}
        )
        return JsonResponse(
            {
                "serviceId": service_id,
                "transId": trans_id,
                "status": "OK",
                "transTime": round(transaction.created_at.timestamp() * 1000),
            },
            status=200
        )

    @staticmethod
    def process_confirm(data):
        service_id = data.get("serviceId")
        timestamp = data.get("timestamp")
        trans_id = data.get("transId")
        payment_source = data.get("paymentSource")
        tariff = data.get("tariff")
        #
        if not service_id_valid(service_id):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10006}, status=400
            )
        if (
            not isinstance(timestamp, int) or
            not isinstance(trans_id, str) or
            not isinstance(payment_source, str)
        ):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10002}, status=400
            )
        #
        try:
            transaction = models.Transaction.objects.get(
                transaction_id=trans_id
            )
        except models.Transaction.DoesNotExist:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10014},
                status=400
            )
        #
        if transaction.status == models.Transaction.StatusChoices.canceled:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10015},
                status=400
            )
        elif transaction.status == models.Transaction.StatusChoices.paid:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10016},
                status=400
            )
        #
        TransactionManager.update_instance(
            transaction,
            {
                "status": models.Transaction.StatusChoices.paid,
                "additional_parameters": {
                    "payment_source": payment_source,
                    "paid_from_service_at": timestamp
                },
                "is_paid": True,
            }
        )
        return JsonResponse(
            {
                "serviceId": service_id,
                "transId": trans_id,
                "status": "CONFIRMED",
                "confirmTime": round(transaction.updated_at.timestamp() * 1000),
                "amount": transaction.amount,
            },
            status=200
        )

    @staticmethod
    def process_reverse(data):
        service_id = data.get("serviceId")
        timestamp = data.get("timestamp")
        trans_id = str(data.get("transId"))
        #
        if not service_id_valid(service_id):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10006}, status=400
            )
        if not isinstance(timestamp, int):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10002}, status=400
            )
        #
        try:
            transaction = models.Transaction.objects.get(
                transaction_id=trans_id
            )
        except models.Transaction.DoesNotExist:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10014},
                status=400
            )
        #
        if transaction.status == models.Transaction.StatusChoices.canceled:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10018},
                status=400
            )
        elif transaction.status == models.Transaction.StatusChoices.paid:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10017},
                status=400
            )
        #
        TransactionManager.update_instance(
            transaction,
            {
                "status": models.Transaction.StatusChoices.canceled,
                "additional_parameters": {
                    "canceled_from_service_at": timestamp,
                },
            }
        )
        return JsonResponse(
            {
                "serviceId": service_id,
                "transId": trans_id,
                "status": "REVERSED",
                "reverseTime": round(transaction.updated_at.timestamp() * 1000),
                "amount": transaction.amount,
            },
            status=200
        )

    @staticmethod
    def process_status(data):
        service_id = data.get("serviceId")
        timestamp = data.get("timestamp")
        trans_id = str(data.get("transId"))
        #
        if not service_id_valid(service_id):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10006}, status=400
            )
        if not isinstance(timestamp, int):
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10002}, status=400
            )
        #
        try:
            transaction = models.Transaction.objects.get(
                transaction_id=trans_id
            )
        except models.Transaction.DoesNotExist:
            return JsonResponse(
                {"status": "FAILED", "errorCode": 10014},
                status=400
            )
        #
        if transaction.status == models.Transaction.StatusChoices.canceled:
            status = "REVERSED"
        elif transaction.status == models.Transaction.StatusChoices.paid:
            status = "CONFIRMED"
        else:
            status = "CREATED"
        #
        return JsonResponse(
            {
                "serviceId": service_id,
                "transId": trans_id,
                "status": status,
                "transTime": round(transaction.created_at.timestamp() * 1000),
                "confirmTime": transaction.additional_parameters.get(
                    "paid_from_service_at"
                ),
                "reverseTime": transaction.additional_parameters.get(
                    "canceled_from_service_at"
                ),
                "amount": transaction.amount,
            },
            status=200
        )

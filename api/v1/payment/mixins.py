import hmac
import hashlib
import base64
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class AlifSignatureAuthMixin:

    @staticmethod
    def sign(body):
        return base64.b64encode(
            hmac.new(settings.ALIF_SECRET_KEY, body, hashlib.sha256).digest()
        )

    def authenticate(self, request):
        alif_signature = request.headers.get("Signature")
        return self.sign(request.body) == alif_signature

    def dispatch(self, request, *args, **kwargs):
        if not self.authenticate(request):
            return Response(
                {"detail": "Invalid or missing signature."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().dispatch(request, *args, **kwargs)

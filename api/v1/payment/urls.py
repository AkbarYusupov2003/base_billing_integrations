from django.http import JsonResponse
from django.urls import path

from api.v1.payment import views


urlpatterns = [
    path("generate-link/uzum", views.GenerateUzumLinkView.as_view()),
    path("uzum-merchant/check", views.UzumCheckAPIView.as_view()), # ✅
    path("uzum-merchant/create", views.UzumCreateAPIView.as_view()), # ✅
    path("uzum-merchant/confirm", views.UzumConfirmAPIView.as_view()), # ✅
    path("uzum-merchant/reverse", views.UzumReverseAPIView.as_view()), # ✅
    path("uzum-merchant/status", views.UzumStatusAPIView.as_view()), # ✅
    #
    path("generate-link/alif", views.GenerateAlifLinkView.as_view()),
    path("alif-merchant/get-invoice/", views.AlifGetInvoiceAPIView.as_view()),
    path("alif-merchant/refundInvoice/", views.AlifRefundInvoiceAPIView.as_view()),
    path("alif-merchant/sendInvoice/", views.AlifSendInvoiceAPIView.as_view()),
    path("alif-merchant/webhook", views.AlifWebhookAPIView.as_view()),
]

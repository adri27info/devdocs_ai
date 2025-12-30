from django.urls import path

from apps.invoices.views import InvoiceView

urlpatterns = [
    path("", InvoiceView.as_view(), name="invoices"),
]

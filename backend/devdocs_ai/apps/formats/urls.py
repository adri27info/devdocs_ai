from django.urls import path

from apps.formats.views import FormatView

urlpatterns = [
    path("", FormatView.as_view(), name="formats"),
]

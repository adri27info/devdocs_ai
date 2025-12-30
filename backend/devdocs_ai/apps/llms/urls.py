from django.urls import path

from apps.llms.views import LLMView

urlpatterns = [
    path("", LLMView.as_view(), name="llms"),
]

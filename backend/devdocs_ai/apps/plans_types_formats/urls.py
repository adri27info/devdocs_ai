from django.urls import path

from apps.plans_types_formats.views import PlanTypeFormatView

urlpatterns = [
    path("", PlanTypeFormatView.as_view(), name="plans_types_formats"),
]

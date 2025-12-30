from django.urls import path

from apps.plans_types.views import PlanTypeView

urlpatterns = [
    path("", PlanTypeView.as_view(), name="plans_types"),
]

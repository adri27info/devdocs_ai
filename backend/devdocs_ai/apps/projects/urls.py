from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectViewset

router = DefaultRouter()
router.register(r"", ProjectViewset, basename="projects")

urlpatterns = router.urls

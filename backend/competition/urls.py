from rest_framework_nested import routers

from .views import CompetitionViewset

router = routers.DefaultRouter()
router.register('', CompetitionViewset, basename='competition')

urlpatterns = router.urls
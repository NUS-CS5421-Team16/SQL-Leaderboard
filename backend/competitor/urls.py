from rest_framework_nested import routers

from competitor.views import CompetitorViewset

router = routers.DefaultRouter()
router.register('', CompetitorViewset, basename='competitor')

urlpatterns = router.urls
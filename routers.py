from rest_framework import routers
from user.viewsets import UserViewSet,RegisterViewSet
from dashboard.views import PortScannerViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"edit", UserViewSet, basename="user-edit")

router.register(r"register", RegisterViewSet, basename="register")
router.register(r'portscanner', PortScannerViewSet, basename='port-scanner')


# router.register(r"recipesview", RecipesViewSet, basename="RecipesViewSet")

urlpatterns = [
    *router.urls,
]

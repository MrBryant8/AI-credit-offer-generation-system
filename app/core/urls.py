from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CreditOfferViewSet, ModeratorViewSet

router = DefaultRouter()
router.register(r'customers', ClientViewSet)
router.register(r'applications', CreditOfferViewSet)
router.register(r'moderators', ModeratorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

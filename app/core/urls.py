from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CreditOfferViewSet, UserViewSet, ChatViewSet, MessageViewSet, LoanViewSet
from .views.general import home_view, login_view

router = DefaultRouter()
router.register(r'customers', ClientViewSet)
router.register(r'applications', CreditOfferViewSet)
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'loans', LoanViewSet)


urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path('api/', include(router.urls))
]

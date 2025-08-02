from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CreditOfferViewSet, UserViewSet, ChatViewSet, MessageViewSet, LoanViewSet
from .views.general import HomePageView, LoginPageView, SignUpPageView

router = DefaultRouter()
router.register(r'customers', ClientViewSet)
router.register(r'applications', CreditOfferViewSet)
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'loans', LoanViewSet)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("sign-up/", SignUpPageView.as_view(), name="signup"),
    path('api/', include(router.urls))
]

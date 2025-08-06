from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'customers', ClientViewSet)
router.register(r'credit-offers', CreditOfferViewSet)
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'loans', LoanViewSet)


urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("sign-up/", SignUpPageView.as_view(), name="signup"),
    path("home/", HomePageView.as_view(), name="home"),
    path("my-offers/", MyOffersView.as_view(), name="my_offers"),
    path('offers/<int:pk>/', CreditOfferDetailView.as_view(), name='offer_detail'),
    path('offer/<int:pk>/accept/', AcceptOfferView.as_view(), name='accept_offer'),
    path('offer/<int:pk>/reject/', RejectOfferView.as_view(), name='reject_offer'),
    path('offer/<int:pk>/edit-email/', EditOfferEmailView.as_view(), name='edit_offer_email'),
    path('offer/<int:pk>/send-email/', SendOfferEmailView.as_view(), name='send_offer_email'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path("manage/", ManageView.as_view(), name="manage"),
    path("manage/suggested-offers", ModeratorOffersView.as_view(), name="moderator_offers"),
    path("manage/add-customer", AddCustomerView.as_view(), name="add_customer"),
    path('api/', include(router.urls))
]

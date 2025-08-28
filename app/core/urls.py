from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'customers', ClientViewSet)
router.register(r'credit-offers', CreditOfferViewSet)
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'agent-feedbacks', AgentFeedbackViewSet)


urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("sign-up/", SignUpPageView.as_view(), name="signup"),
    path("home/", HomePageView.as_view(), name="home"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("my-offers/", MyOffersView.as_view(), name="my_offers"),
    path('offers/<int:pk>/', CreditOfferDetailView.as_view(), name='offer_detail'),
    path('offer/<int:pk>/accept/', AcceptOfferView.as_view(), name='accept_offer'),
    path('offer/<int:pk>/reject/', RejectOfferView.as_view(), name='reject_offer'),
    path('offer/<int:pk>/edit-email/', EditOfferEmailView.as_view(), name='edit_offer_email'),
    path('offer/<int:pk>/send-email/', SendOfferEmailView.as_view(), name='send_offer_email'),
    path("offer/<int:pk>/chat", ChatView.as_view(), name="chat_page"),
    path('chat/<int:offer_id>/chat/save_and_reset/', save_and_reset_chat, name='save_and_reset_chat'),
    path('chat/<int:offer_id>/chat/reset/', reset_chat, name='reset_chat'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path("manage/", ManageView.as_view(), name="manage"),
    path("manage/suggested-offers", ModeratorOffersView.as_view(), name="moderator_offers"),
    path("manage/add-customer", AddCustomerView.as_view(), name="add_customer"),
    path("manage/edit-customers/", EditCustomersView.as_view(), name="edit_customers"),
    path("manage/edit-customer/<int:pk>/", EditCustomerView.as_view(), name="edit_customer"),
    path("manage/edit-customer/<int:pk>/deactivate/", DeactivateCustomerView.as_view(), name="deactivate_customer"),
    path("manage/view-declined-customers/", DeclinedClientsView.as_view(), name="declined_clients"),
    path("manage/view-agent-feedback/", AgentFeedbackView.as_view(), name="agent_feedback"),
    path("manage/feedback/<int:pk>/decline/", AgentFeedbackDeclineView.as_view(), name="decline_agent_feedback"),
    path("manage/feedback/<int:pk>/report/", AgentFeedbackReportView.as_view(), name="report_agent_feedback"),
    path("create-email/", write_email, name="create_email"),
    path('api/', include(router.urls))
]

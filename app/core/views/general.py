import time
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import *
from ..models import *
from ..services.custom_api import *
from django.core.paginator import Paginator


class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html', )


class LoginPageView(FormView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = UserLoginForm(request.POST)
        error_message = None
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('/home')
            else:
                error_message = 'Invalid email or password'

        return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('/')


class SignUpPageView(FormView):
    def get(self, request):
        return render(request, 'sign-up.html')

    def post(self, request):
        form = UserRegisterForm(request.POST)
        error_message = None
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = add_new_user(first_name=first_name, last_name=last_name, email=email, password=password)
                login(request, user)
                return redirect('/home', )
            except Exception as e:
                error_message = str(e)

        return render(request, 'sign-up.html', {'error_message': error_message})


class MyOffersView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        credit_offers = fetch_credit_offers_per_user(user_id=request.user.id)
        return render(request, 'my-offers.html', {'credit_offers': credit_offers})


class CreditOfferDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = CreditOffer
    template_name = 'offer-detail.html'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = context['offer']
        context['expiry_date'] = offer.created_at + timedelta(weeks=1)

        storage = get_messages(self.request)
        messages_list = list(storage)
        context['last_message'] = messages_list[-1] if messages_list else None

        return context
    

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        # Optional: render a custom 403 template or return a basic forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        model_name = request.GET.get('model', 'users').lower()
        page = request.GET.get('page', 1)

        model_map = {
            'users': User,
            'clients': Client,
            'loans': Loan,
            'offers': CreditOffer,
            'messages': Message,
            'chats': Chat,
        }

        model = model_map.get(model_name)
        if not model:
            return render(request, 'admin/tables/empty_table.html', {'message': 'Model not found!'})

        queryset = model.objects.all().order_by('id')

        paginator = Paginator(queryset, 5)  # 10 items per page
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'model_name': model_name,
        }
        template_name = f'admin/tables/{model_name}_table.html'
        return render(request, template_name, context)


class ManageView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        # Optional: render a custom 403 template or return a basic forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        return render(request, 'manage.html')


class ModeratorOffersView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        # Optional: render a custom 403 template or return a basic forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        deactivate_old_credit_offers()
        credit_offers = CreditOffer.objects.filter(is_active=True)
        return render(request, 'suggested-offers.html', {'credit_offers': credit_offers})

class EditOfferEmailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login'
    
    model = CreditOffer
    form_class = EditOfferEmailForm
    template_name = 'creditoffer_edit_email.html'

    def get_success_url(self):
        return reverse_lazy('offer_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Only allow moderators
        return self.request.user.is_moderator

    def handle_no_permission(self):
        # Optionally redirect or raise 403
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("Sie haben keine Berechtigung, dieses Angebot zu bearbeiten.")
        return super().handle_no_permission()

class SendOfferEmailView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"
    
    def test_func(self):
        # For example: only moderators can send emails
        return self.request.user.is_moderator

    def post(self, request, pk):
        offer = get_object_or_404(CreditOffer, pk=pk)
        
        # Implement your email sending logic here
        # e.g., using Django's send_mail or other email service

        # Example (pseudo):
        # send_offer_email(offer)

        msg.success(request, f"E-Mail für Angebot #{offer.id} wurde erfolgreich versandt.")

        # needs more
        return redirect('offer_detail', pk=pk)
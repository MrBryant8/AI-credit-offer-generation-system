from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import *
from ..models import *
from ..services.database_manager import add_new_user, fetch_credit_offers_per_user
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

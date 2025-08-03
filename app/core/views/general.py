from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import *
from ..models import CreditOffer
from ..services.database_manager import add_new_user, fetch_credit_offers_per_user


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
        return render(request, 'my-offers.html')


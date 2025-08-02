from http.client import HTTPResponse

from django.shortcuts import render
from django.views import View
from django.views.generic import FormView



class HomePageView(View):
    def get(self, request):
        return render(request, 'index.html')


class LoginPageView(FormView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, password)
        return HTTPResponse("Wrong email or password")

class SignUpPageView(FormView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, password)
        return HTTPResponse({'email': email, 'password': password})
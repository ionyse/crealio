from django.shortcuts import render
from crealio.users.decorators import main_site


@main_site
def index(request):
    return render(request, 'users/home.html')


@main_site
def sign_in(request):
    return render(request, 'users/sign-in.html')

from re import A
from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login, authenticate

from django.contrib.auth import logout as auth_logout

from .models import Weather, SearchHistory

from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, WeatherForm

from django.contrib.auth.models import User

from core.settings import API_WEATHER_KEY

import requests

API_KEY = API_WEATHER_KEY


def index(request):

    weather = None

    if request.method == "POST":
        form = WeatherForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data["city"]
            response = requests.get(API_KEY.format(city=city))
            data = response.json()

            if response.status_code == 200:
                weather = Weather.objects.create(
                    city=city,
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    description=data["weather"][0]["description"],
                )

                SearchHistory.objects.create(
                    user=request.user,
                    city=weather.city,
                    temperature=weather.temperature,
                    description=weather.description,
                )
    else:
        form = WeatherForm()

    return render(request, "weather/index.html", {"form": form, "weather": weather})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            user = User.objects.filter(email__iexact=email).first()

            if user is not None and user.check_password(password) and user.is_active:
                auth_login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                return redirect("index")

            form.add_error(None, "Неправильний email або пароль.")

    else:
        form = LoginForm()

    return render(request, "weather/login.html", {"form": form})


def register_view(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()

    return render(request, "weather/register.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("index")


@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by("-search_date")
    return render(request, "weather/history.html", {"history": history})

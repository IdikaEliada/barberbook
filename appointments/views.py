from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

from .models import Barber, Service, Appointment
from .forms import RegisterForm, AppointmentForm


def home(request):
    return render(request, "appointments/home.html")


def service_list(request):
    services = Service.objects.all()
    return render(request, "appointments/services.html", {"services": services})


def barber_list(request):
    barbers = Barber.objects.all()
    return render(request, "appointments/barbers.html", {"barbers": barbers})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created. Welcome to BarberBook!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "appointments/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "appointments/login.html", {"form": form})


def user_logout(request):
    auth_logout(request)
    return redirect("home")


@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.status = "pending"
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect("my_appointments")
    else:
        form = AppointmentForm()
    return render(request, "appointments/book_appointment.html", {"form": form})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(customer=request.user)
    return render(request, "appointments/my_appointments.html", {"appointments": appointments})


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user)
    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.save()
        messages.success(request, "Appointment cancelled.")
        return redirect("my_appointments")
    return render(request, "appointments/cancel_confirm.html", {"appointment": appointment})


def is_admin(user):
    return user.is_staff


@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, "You do not have access to the admin dashboard.")
        return redirect("home")
    appointments = Appointment.objects.all()
    return render(request, "appointments/admin_dashboard.html", {"appointments": appointments})


@login_required
def confirm_appointment(request, pk):
    if not is_admin(request.user):
        return redirect("home")
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = "confirmed"
    appointment.save()
    return redirect("admin_dashboard")

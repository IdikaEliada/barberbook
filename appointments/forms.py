from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "barber", "date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned = super().clean()
        barber = cleaned.get("barber")
        date = cleaned.get("date")
        time = cleaned.get("time")
        if barber and date and time:
            clash = Appointment.objects.filter(
                barber=barber, date=date, time=time
            ).exclude(status="cancelled")
            if clash.exists():
                raise forms.ValidationError(
                    "That barber is already booked at this date and time. Please choose another slot."
                )
        return cleaned

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="services"),
    path("barbers/", views.barber_list, name="barbers"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("book/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("appointments/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("appointments/<int:pk>/confirm/", views.confirm_appointment, name="confirm_appointment"),
]

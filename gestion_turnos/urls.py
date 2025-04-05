from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('soporte/', views.dashboard_soporte, name='dashboard_soporte'),
    path('admin-turnos/', views.dashboard_admin, name='dashboard_admin'),
]
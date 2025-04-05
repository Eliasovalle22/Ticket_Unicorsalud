from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PersonalSoporte

# Define un Inline para PersonalSoporte
class PersonalSoporteInline(admin.StackedInline):
    model = PersonalSoporte
    can_delete = False
    verbose_name_plural = "Información de Soporte"

# Extiende UserAdmin para incluir el inline
class CustomUserAdmin(UserAdmin):
    inlines = (PersonalSoporteInline,)

# Registra el modelo personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
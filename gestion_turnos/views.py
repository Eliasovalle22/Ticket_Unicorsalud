from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Estudiante, Turno, PersonalSoporte
from .forms import TurnoForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
import logging
from django.contrib import messages
import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .resources import TurnoResource
from django.http import HttpResponse




#
# ---------------------------- VISTA PARA ESTUDIANTES ---------------------------------
#

@login_required
def dashboard_estudiante(request):
    try:
        estudiante = Estudiante.objects.get(codigo=request.user.username)
    except Estudiante.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.estudiante = estudiante
            turno.save()
            messages.success(request, f"Turno solicitado con éxito (ID: {turno.id})")
            return redirect('dashboard_estudiante')
    else:
        form = TurnoForm()

    turnos = Turno.objects.filter(estudiante=estudiante).order_by('-fecha_solicitud')
    return render(request, 'gestion_turnos/dashboard_estudiante.html', {'form': form, 'turnos': turnos})


#
# ---------------------------- VISTA PARA SOPORTE ---------------------------------
#

# Decorador para restringir acceso solo a personal de soporte
def es_personal_soporte(user):
    return hasattr(user, 'personalsoporte')

@login_required
@user_passes_test(es_personal_soporte)
@login_required
def dashboard_soporte(request):
    turnos = Turno.objects.all().order_by('fecha_solicitud')
    
    if request.method == 'POST':
        turno_id = request.POST.get('turno_id')
        accion = request.POST.get('accion')
        turno = Turno.objects.get(id=turno_id)
        if accion == 'atender':
            turno.estado = 'atendido'
            turno.atendido_por = request.user.personalsoporte
            turno.fecha_atencion = timezone.now()
            messages.success(request, f"Turno {turno.id} marcado como atendido.")
        elif accion == 'finalizar':
            turno.estado = 'finalizado'
            messages.success(request, f"Turno {turno.id} finalizado.")
        turno.save()
        return redirect('dashboard_soporte')
    
    return render(request, 'gestion_turnos/dashboard_soporte.html', {'turnos': turnos})


#
# ---------------------------- VISTA GESTIÓN TURNOS ---------------------------------
#

@staff_member_required
def dashboard_admin(request):
    turnos = Turno.objects.all()
    total_turnos = turnos.count()
    turnos_espera = turnos.filter(estado='en_espera').count()
    turnos_atendidos = turnos.filter(estado='atendido').count()
    turnos_finalizados = turnos.filter(estado='finalizado').count()
    
    if request.method == 'POST':
        if 'export_csv' in request.POST:
            # Exportar a CSV
            turno_resource = TurnoResource()
            dataset = turno_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="turnos.csv"'
            return response
        elif 'export_pdf' in request.POST:
            # Exportar a PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.setFont("Helvetica", 12)
            p.drawString(100, 750, "Reporte de Turnos")
            y = 700
            for turno in turnos:
                p.drawString(50, y, f"ID: {turno.id} | Estudiante: {turno.estudiante.nombre} | Tipo: {turno.tipo_turno} | Estado: {turno.estado}")
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 750
            p.showPage()
            p.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="turnos.pdf"'
            return response

    return render(request, 'gestion_turnos/dashboard_admin.html', {
        'total_turnos': total_turnos,
        'turnos_espera': turnos_espera,
        'turnos_atendidos': turnos_atendidos,
        'turnos_finalizados': turnos_finalizados,
        'turnos': turnos,
    })
    
    
#
# ---------------------------- VISTA ROLES ---------------------------------
#

# Configura un logger básico
logger = logging.getLogger(__name__)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            logger.info(f"Usuario logueado: {user.username}, is_staff: {user.is_staff}, tiene personalsoporte: {hasattr(user, 'personalsoporte')}")
            # Redirigir según el rol
            if user.is_staff:
                logger.info("Redirigiendo a dashboard_admin")
                return redirect('dashboard_admin')
            elif hasattr(user, 'personalsoporte'):
                logger.info("Redirigiendo a dashboard_soporte")
                return redirect('dashboard_soporte')
            else:
                try:
                    Estudiante.objects.get(codigo=user.username)
                    logger.info("Redirigiendo a dashboard_estudiante")
                    return redirect('dashboard_estudiante')
                except Estudiante.DoesNotExist:
                    logger.warning(f"No se encontró estudiante para {user.username}, redirigiendo a login")
                    return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'gestion_turnos/login.html', {'form': form})



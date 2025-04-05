from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['tipo_turno', 'motivo', 'descripcion']
        widgets = {
            'tipo_turno': forms.Select(choices=[
                ('inscripcion', 'Inscripción'),
                ('consulta', 'Consulta'),
                ('reclamo', 'Reclamo'),
            ]),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
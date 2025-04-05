from import_export import resources
from .models import Turno

class TurnoResource(resources.ModelResource):
    class Meta:
        model = Turno
        fields = ('id', 'estudiante__nombre', 'tipo_turno', 'motivo', 'estado', 'atendido_por__nombre', 'fecha_solicitud', 'fecha_atencion')
        export_order = ('id', 'estudiante__nombre', 'tipo_turno', 'motivo', 'estado', 'atendido_por__nombre', 'fecha_solicitud', 'fecha_atencion')
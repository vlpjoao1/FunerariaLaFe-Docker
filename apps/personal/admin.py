from django.contrib import admin
from .models import Personal, RegistroDeAsistencia, HistorialPersonal
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class PersonalResource(resources.ModelResource):
	class Meta:
		model=Personal

class CategoriaPersonal(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['cedula','nombres','apellidos','telefono']
	list_display = ('cedula','nombres','apellidos','telefono','fecha_de_ingreso')
	resource_class=PersonalResource

class RegistroDeAsistenciaResource(resources.ModelResource):
	class Meta:
		model=RegistroDeAsistencia

class CategoriaAsistencia(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['empleado__cedula','si_trabajo','hora_entrada','fecha_entrada','hora_salida','fecha_salida']
	list_display = ('empleado','si_trabajo','hora_entrada','fecha_entrada','hora_salida','fecha_salida')
	resource_class=RegistroDeAsistenciaResource

class HistorialPersonalResource(resources.ModelResource):
	class Meta:
		model=HistorialPersonal

class CategoriaHistorial(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['historial_empleado__cedula','acotacion','fecha_acotacion']
	list_display = ('historial_empleado','acotacion','fecha_acotacion')
	resource_class=HistorialPersonalResource


admin.site.register(Personal, CategoriaPersonal)
admin.site.register(RegistroDeAsistencia,CategoriaAsistencia)
admin.site.register(HistorialPersonal, CategoriaHistorial)
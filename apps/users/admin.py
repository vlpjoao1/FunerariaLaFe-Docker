from django.contrib import admin
from django.contrib.auth.models import Permission
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Usuario, Bitacora, Inicio
# Register your models here.

class UsuarioResource(resources.ModelResource):
	class Meta:
		model=Usuario

class CategoriaUsuario(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['username','email','nombre','apellidos']
	list_display = ('username','email','nombre','apellidos')
	resource_class=UsuarioResource

class BitacoraResource(resources.ModelResource):
	class Meta:
		model=Bitacora

class CategoriaBitacora(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['usuario','accion','fecha_accion']
	list_display = ('usuario','accion','fecha_accion')
	resource_class=BitacoraResource

admin.site.register(Usuario, CategoriaUsuario)
admin.site.register(Bitacora, CategoriaBitacora)
admin.site.register(Inicio)
admin.site.register(Permission)
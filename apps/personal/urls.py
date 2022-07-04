from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .views import (ListarPersonal,CrearPersonal,ActualizarPersonal,EliminarPersonal,
InicioBitacoraPersonal, ListarBitacoraPersonal, CrearBitacoraPersonal, AgregarHoraSalidaPersonal,EliminarBitacoraPersonal,
 InicioHistorial, ListarHistorial, CrearHistorial, EditarHistorial, EliminarHistorial, ReporteAsistencia
 )
 
 
urlpatterns=[
	path('Listar/', login_required(ListarPersonal.as_view()), name='listar_personal'),
	path('Crear/', login_required(CrearPersonal.as_view()), name='crear_personal'),
	path('Editar/<int:pk>/', login_required(ActualizarPersonal.as_view()), name='editar_personal'),
	path('Eliminar/<int:pk>/', login_required(EliminarPersonal.as_view()), name='eliminar_personal'),
	path('Bitacora/inicio/', login_required(InicioBitacoraPersonal.as_view()), name='inicio_bitacora_personal'),
	path('Bitacora/Listar/', login_required(ListarBitacoraPersonal.as_view()), name='listar_bitacora_personal'),
	path('Bitacora/Crear/', login_required(CrearBitacoraPersonal.as_view()), name='crear_bitacora_personal'),
	path('Bitacora/Editar/<int:pk>/', login_required(AgregarHoraSalidaPersonal.as_view()), name='editar_bitacora_personal'),
	path('Bitacora/Eliminar/<int:pk>/', login_required(EliminarBitacoraPersonal.as_view()), name='eliminar_bitacora_personal'),
	path('Historial/inicio/', login_required(InicioHistorial.as_view()), name='inicio_historial_personal'),
	path('Historial/Listar/', login_required(ListarHistorial.as_view()), name='crear_historial_personal'),
	path('Historial/Crear/', login_required(CrearHistorial.as_view()), name='crear_historial_personal'),
	path('Historial/Editar/<int:pk>/', login_required(EditarHistorial.as_view()), name='editar_historial_personal'),
	path('Historial/Eliminar/<int:pk>/', login_required(EliminarHistorial.as_view()), name='eliminar_historial_personal'),
	path('Reporte/Asistencias/', login_required(ReporteAsistencia.as_view()), name='reporte_asistencia')
] 


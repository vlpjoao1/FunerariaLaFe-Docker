from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ListarBitacora, CrearUsuario, RecuperarUsuario, InicioUsuarios, ListarUsuarios, CrearUsuarios, EditarUsuario, EliminarUsuario
urlpatterns=[
	path('Crear/', CrearUsuario.as_view(), name='crear_usuario'),
	path('Recuperar/', RecuperarUsuario.as_view(), name='recuperar_usuario'),
	path('Bitacora/Listar/', login_required(ListarBitacora.as_view()), name='listar_bitacora'),
	path('Inicio/', login_required(InicioUsuarios.as_view()), name='inicio_usuarios'),
	path('Listar/', login_required(ListarUsuarios.as_view()), name='listar_usuarios'),
	path('CrearUsuario/', CrearUsuarios.as_view(), name='crear_usuarios'),
	path('Editar/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
	path('Eliminar/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario')
]
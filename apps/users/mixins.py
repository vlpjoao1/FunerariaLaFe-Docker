from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

class ValidarPermisosRequeridosMixin(object):
	#permisos requeridos
	permission_required=''
	#dodne va a redirigir en caso de que no tenga permisos
	url_redirect=None

	""" get perm es 'obtiene los permisos'
	Luego los pasarás a un if"""
	def get_perms(self):
		""" isinstance recibe dos parametros, el priemro es
		la varaible, y el segundo es para verificar si la varaible
		es de ese tipo de datos"""
		if isinstance(self.permission_required,str):
			#convierte el permission_required en una tupla
			return (self.permission_required)
		else:
			#en caso de que ya sea una tupla, se retroan igual
			return self.permission_required

	def get_url_redirect(self):
		if self.url_redirect is None:
			return reverse_lazy('login')
		#esto se ejecutará en caso de que no se ejecute el if
		return self.url_redirect

	def dispatch(self, request, *args, **kwargs):
		# verifica si el usuario tiene los permisos.
		# Has perms es "tiene permisos" y los obtiene de
		# get_perms, la otra función
		if request.user.has_perms(self.get_perms()):
			return super().dispatch(request, *args, **kwargs)
		messages.error(request,'No tienes permisos para realizar esta acción, fuiste redirigido al inicio')
		return redirect(self.get_url_redirect())
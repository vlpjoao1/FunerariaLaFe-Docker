import json
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView,DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from apps.users.mixins import ValidarPermisosRequeridosMixin
from .forms import FormularioLogin, FormularioUsuario, ResetPasswordForm
from .models import Usuario, Bitacora, Inicio

# usuarios dentro del programa -----------------------------------------------------
class InicioUsuarios(ValidarPermisosRequeridosMixin,TemplateView):
	template_name='users/listar_usuarios.html'

class ListarUsuarios(ValidarPermisosRequeridosMixin,ListView):
	model=Usuario

	def get_queryset(self, **kwargs):
		return self.model.objects.all()

	def get_context_data(self, **kwargs):
		contexto={}
		contexto['Usuario']=self.get_queryset()
		return contexto

	def get(self,request,*args,**kwargs):
		if request.is_ajax():
			data=serialize('json', self.get_queryset())
			return HttpResponse(data,'aplication/json')

class CrearUsuarios(ValidarPermisosRequeridosMixin,CreateView):
	model=Usuario
	form_class=FormularioUsuario
	template_name='users/crear_usuario.html'
	
	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST)
			if form.is_valid():
				form.save()
				mensaje = f'{self.model.__name__} registrado correctamente!'
				error = 'No hay error!'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=201
				print(response.content)
				return response
			else:
				mensaje=f'{self.model.__name__} no se ha podido registrar!'
				error= form.errors
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response				
		else:
			return redirect('usuarios:listar_usuario')

class EditarUsuario(ValidarPermisosRequeridosMixin,UpdateView):
	model=Usuario
	form_class=FormularioUsuario
	template_name='users/editar_usuario.html'

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['Usuario']=Usuario.objects.all()
		return context

	def post(self, request, *args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST, instance=self.get_object())
			if form.is_valid():
				form.save()
				mensaje=f'{self.model.__name__} Actualizado Correctamente!'
				error='No hay errores!'
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=201
				return response
			else:
				mensaje=f'{self.model.__name__} no se puede actualizar!'
				error=form.errors
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
		else:
			return redirect('usuarios:listar_usuario')			

class EliminarUsuario(ValidarPermisosRequeridosMixin,DeleteView):
	model=Usuario
	template_name='users/eliminar_usuario.html'

	def get_context_data(self,**kwargs):
		context={}
		context['Usuario']=self.get_object()
		return context

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name, self.get_context_data())

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			eliminar=str(self.get_object())
			usuario=request.user.username
			if usuario==eliminar:
				mensaje=f'El usuario "{usuario}" no se puede Eliminar debido a que es el usuario con el que actualmente tienes sesión iniciada!'
				error='El usuario o se puede Eliminar debido a que es el usuario con el que actualmente tienes sesión iniciada!'
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
			elif usuario!=eliminar:
				usuarioEliminar=self.get_object()
				usuarioEliminar.delete()
				mensaje=f'{self.model.__name__} Eliminado Correctamente!'
				error='No hay errores!'
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=201
				return response
		else:
			return redirect('usuarios:listar_usuario')	
# ------------------------------------------------------------------------------------

class Login(FormView):
	template_name='login.html'
	form_class=FormularioLogin
	success_url=reverse_lazy('index')

	@method_decorator(csrf_protect)
	@method_decorator(never_cache)

	def dispatch(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:	
			return super(Login,self).dispatch(request,*args,**kwargs)
	def form_valid(self,form):
		login(self.request,form.get_user())
		return super(Login,self).form_valid(form)

	def get(self,request,*args,**kwargs):
		if Usuario.objects.filter().exists():
			return render(request, self.template_name, {'form':self.form_class})
		else:
			return redirect('usuarios:crear_usuario')

class Inicio(ListView):
	model=Inicio
	template_name='index.html'

	def get_queryset(self,**kwargs):
		return self.model.objects.all()
	
def Logout(request):
	logout(request)
	return HttpResponseRedirect('/accounts/login/')

class CrearUsuario(CreateView):
	model=Usuario
	template_name='usuarios/crear_usuario.html'
	form_class=FormularioUsuario

	def get(self,request,*args,**kwargs):
		if Usuario.objects.all().exists():
			return redirect('login')
		else:
			return render(request,self.template_name,{'form':self.form_class})

	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST)
		if form.is_valid():
			formulario=form.save(commit=False)
			clave=make_password(form.cleaned_data.get('password1'))
			usuario=form.cleaned_data.get('username')
			nuevo_usuario=Usuario(
				password=clave,
				username=form.cleaned_data.get('username'),
				is_superuser=True,
				nombre=form.cleaned_data.get('nombre'),
				apellidos=form.cleaned_data.get('apellidos'),
				pregunta=form.cleaned_data.get('pregunta'),
				respuesta=form.cleaned_data.get('respuesta'),
				is_active=True,
				is_staff=True,
				email=form.cleaned_data.get('email')
			)
			nuevo_usuario.save()
			messages.success(request,f'El usuario {usuario} ha sido creado con éxito!')
			return redirect('login')
		else:
			return render(request,self.template_name,{'form':self.form_class,'error':form.errors})

class RecuperarUsuario(FormView):
	model=Usuario
	template_name='usuarios/recuperar_usuario.html'
	form_class=ResetPasswordForm

	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST)
		if form.is_valid():
			""" Los formularios solo obtienen el cleaned_data luego de ser llamados con is_valid()"""
			usuario=form.cleaned_data.get('username')
			query=self.model.objects.filter(username=usuario).values()
			if self.model.objects.filter(username=usuario).exists():
				query=self.model.objects.filter(username=usuario).values()
				if (form.cleaned_data.get('pregunta') == query[0]['pregunta']) and (form.cleaned_data.get('respuesta') == query[0]['respuesta']):
					clave=make_password(form.cleaned_data.get('password1'))
					recuperar_usuario=Usuario(
						id=query[0]['id'],
						password=clave,
						username=query[0]['username'],
						is_superuser=True,
						nombre=query[0]['nombre'],
						apellidos=query[0]['apellidos'],
						pregunta=query[0]['pregunta'],
						respuesta=query[0]['respuesta'],
						is_active=query[0]['is_active'],
						is_staff=query[0]['is_staff'],
						imagen=query[0]['imagen'],
						email=query[0]['email']
					)
					""" Así puedo hashear la contraseña
					#recuperar_usuario.set_password(recuperar_usuario.password)"""
					recuperar_usuario.save()
					messages.success(request,f'El usuario {usuario} ha sido recuperado exitosamente!')
					return redirect('login')
				else:
					if form.cleaned_data.get('pregunta') != query[0]['pregunta']:
						return render(request, self.template_name, {'form':self.form_class,'error':'La pregunta de seguridad no coincide '})
					elif form.cleaned_data.get('respuesta') == query[0]['respuesta']:
						return render(request, self.template_name, {'form':self.form_class,'error':'La respuesta de seguridad no coincide '})
		else:
			return render(request, self.template_name, {'form':self.form_class,'error':form.errors})

class ListarBitacora(ListView):
	model=Bitacora
	template_name='usuarios/bitacora_usuario.html'

	def get_queryset(self,**kwargs):
		return self.model.objects.all()
import os
from ProyectoPatricia.wsgi import *
from ProyectoPatricia import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import get_template
from weasyprint import HTML, CSS
from apps.users.mixins import ValidarPermisosRequeridosMixin
from apps.users.models import Bitacora
import datetime
from time import gmtime, strftime
from .models import Personal, RegistroDeAsistencia, HistorialPersonal
from .forms import FormularioPersonal, FormularioBitacora,FormularioHistorial, ReporteForm


# Create your views here.

class ListarPersonal(ValidarPermisosRequeridosMixin,ListView):
	permission_required=('personal.view_personal',)
	model=Personal
	template_name='personal/listar_personal.html'

	def get_queryset(self,**kwargs):
		return self.model.objects.all()

class CrearPersonal(ValidarPermisosRequeridosMixin,CreateView):
	model=Personal
	form_class=FormularioPersonal
	template_name='personal/crear_personal.html'

	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST, files=request.FILES)
		if form.is_valid():
			formulario=form.save(commit=False)
			fecha_actual=datetime.datetime.now()
			if formulario.fecha_de_ingreso>fecha_actual.date():
				messages.warning(request, 'La fecha de ingreso no debe ser mayor a la fecha actual.')
				return redirect('personal:listar_personal')
			else:
				formulario.save()
				nueva_bitacora=Bitacora(
					usuario=str(request.user.nombre),
					accion='Agregó un Empleado'
				)
				nueva_bitacora.save()
				messages.success(request,'Personal registrado correctamente.')
				return redirect('personal:listar_personal')
		else:
			messages.warning(request,form.errors)
			return redirect('personal:listar_personal')

class ActualizarPersonal(ValidarPermisosRequeridosMixin,UpdateView):
	model=Personal
	form_class=FormularioPersonal
	template_name='personal/editar_personal.html'

	def get_context_data(self,**kwargs):
		context=super().get_context_data()
		context['Personal']=Personal.objects.all()
		return context


	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST, files=request.FILES, instance=self.get_object())
		if form.is_valid():
			formulario=form.save(commit=False)
			fecha_actual=datetime.datetime.now()
			if formulario.fecha_de_ingreso>fecha_actual.date():
				messages.warning(request, 'La fecha de ingreso no debe ser mayor a la fecha actual.')
				return redirect('personal:listar_personal')
			else:
				formulario.save()
				nueva_bitacora=Bitacora(
					usuario=str(request.user.nombre),
					accion='Actualizó un Empleado'
				)
				nueva_bitacora.save()
				messages.success(request,'Personal Actualizado correctamente.')
				return redirect('personal:listar_personal')
		else:
			messages.warning(request,form.errors)
			return redirect('personal:listar_personal')

class EliminarPersonal(ValidarPermisosRequeridosMixin,DeleteView):
	model=Personal
	template_name='personal/eliminar_personal.html'

	def get_context_data(self,**kwargs):
		context={}
		context['Personal']=self.get_object()
		return context

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,self.get_context_data())

	def post(self,request,*args,**kwargs):
		personal=self.get_object()
		personal.delete()
		nueva_bitacora=Bitacora(
			usuario=str(request.user.nombre),
			accion='Eliminó un Empleado'
		)
		nueva_bitacora.save()
		messages.success(request,'Personal eliminado correctamente.')
		return redirect('personal:listar_personal')




class InicioBitacoraPersonal(ValidarPermisosRequeridosMixin,TemplateView):
	permission_required=('personal.view_registrodeasistencia',)
	template_name='bitacora/listar_bitacora_personal.html'

class ListarBitacoraPersonal(ValidarPermisosRequeridosMixin,ListView):
	permission_required=('personal.view_registrodeasistencia',)
	model=RegistroDeAsistencia

	def get_queryset(self, **kwargs):
		return self.model.objects.all()

	def get_context_data(self, **kwargs):
		contexto={}
		contexto['BitacoraPersonal']=self.get_queryset()
		return contexto

	def get(self,request,*args,**kwargs):
		if request.is_ajax():
			data=serialize('json', self.get_queryset(),use_natural_foreign_keys=True)
			return HttpResponse(data,'aplication/json')

class CrearBitacoraPersonal(ValidarPermisosRequeridosMixin,CreateView):
	model=RegistroDeAsistencia
	form_class=FormularioBitacora
	template_name='bitacora/crear_bitacora_personal.html'


	def post(self, request, *args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST)
			formulario=form.save(commit=False)
			fecha_actual=datetime.datetime.now()
			if fecha_actual.date()<formulario.fecha_entrada:
				mensaje=f'La fecha de entrada no debe ser mayor al día actual'
				error=form.errors
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
			else:
				if form.is_valid():
					form.save()
					nueva_bitacora=Bitacora(
						usuario=str(request.user.nombre),
						accion='Agregó una entrada/salida de empleado'
						)
					nueva_bitacora.save()
					mensaje=f'{self.model.__name__} Registrado Correctamente!'
					error='No hay errores!'
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=201
					return response
				else:
					mensaje=f'{self.model.__name__} no se puede registrar!'
					error=form.errors
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=400
					return response
		else:
			return redirect('personal:inicio_bitacora_personal')

class AgregarHoraSalidaPersonal(ValidarPermisosRequeridosMixin,UpdateView):
	model=RegistroDeAsistencia
	form_class=FormularioBitacora
	template_name='bitacora/editar_bitacora_personal.html'

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['BitacoraPersonal']=RegistroDeAsistencia.objects.all()
		return context

	def post(self, request, *args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST, instance=self.get_object())
			formulario=form.save(commit=False)
			fecha_actual=datetime.datetime.now()
			if fecha_actual.date()<formulario.fecha_entrada:
				mensaje=f'La fecha de entrada no debe ser mayor al día actual'
				error=form.errors
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
			else:
				if form.is_valid():
					form.save()
					nueva_bitacora=Bitacora(
						usuario=str(request.user.nombre),
						accion='Actualizó una entrada/salida de empleado'
						)
					nueva_bitacora.save()
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
			return redirect('personal:inicio_bitacora_personal')


class EliminarBitacoraPersonal(ValidarPermisosRequeridosMixin,DeleteView):
	model=RegistroDeAsistencia
	template_name='bitacora/eliminar_bitacora_personal.html'

	def get_context_data(self,**kwargs):
		context={}
		context['BitacoraPersonal']=self.get_object()
		return context

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name, self.get_context_data())

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			Bitacora_eliminar=self.get_object()
			Bitacora_eliminar.delete()
			nueva_bitacora=Bitacora(
				usuario=str(request.user.nombre),
				accion='Eliminó una entrada/salida de empleado'
			)
			nueva_bitacora.save()
			mensaje=f'{self.model.__name__} Eliminado Correctamente!'
			error='No hay errores!'
			response=JsonResponse({'mensaje':mensaje,'error':error})
			response.status_code=201
			return response
		else:
			return redirect('personal:inicio_bitacora_personal')

class InicioHistorial(ValidarPermisosRequeridosMixin,TemplateView):
	permission_required=('personal.view_historialpersonal',)
	template_name='historial_personal/listar_historial.html'

class ListarHistorial(ValidarPermisosRequeridosMixin,TemplateView):
	permission_required=('personal.view_historialpersonal',)
	model=HistorialPersonal

	def get_queryset(self, **kwargs):
		return self.model.objects.all()

	def get_context_data(self,**kwargs):
		contexto={}
		contexto['HistorialPersonal']=self.get_queryset()
		return contexto

	def get(self,request,*args,**kwargs):
		if request.is_ajax():
			data=serialize('json',self.get_queryset(), use_natural_foreign_keys=True)
			return HttpResponse(data,'aplication/json')
		return HttpResponse('hola')

class CrearHistorial(ValidarPermisosRequeridosMixin,CreateView):
	model=HistorialPersonal
	form_class=FormularioHistorial
	template_name='historial_personal/crear_historial.html'

	def post(self, request, *args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST)
			if form.is_valid():
				formulario=form.save(commit=False)
				fecha_actual=datetime.datetime.now()
				if formulario.fecha_acotacion>fecha_actual.date():
					mensaje=f'La fecha de acotación no debe ser mayor al día actual'
					error=form.errors
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=400
					return response
				else:
					form.save()
					nueva_bitacora=Bitacora(
						usuario=str(request.user.nombre),
						accion='Agregó un historial de empleado'
						)
					nueva_bitacora.save()
					mensaje=f'{self.model.__name__} Registrado Correctamente!'
					error='No hay errores!'
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=201
					return response
			else:
				mensaje=f'{self.model.__name__} no se puede registrar!'
				error=form.errors
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
		else:
			return redirect('personal:inicio_historial_personal')

class EditarHistorial(ValidarPermisosRequeridosMixin,UpdateView):
	model=HistorialPersonal
	form_class=FormularioHistorial
	template_name='historial_personal/editar_historial.html'

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['HistorialPersonal']=HistorialPersonal.objects.all()
		return context

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			form=self.form_class(request.POST, instance=self.get_object())
			if form.is_valid():
				formulario=form.save(commit=False)
				fecha_actual=datetime.datetime.now()
				if formulario.fecha_acotacion>fecha_actual.date():
					mensaje=f'La fecha de acotación no debe ser mayor al día actual'
					error=form.errors
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=400
					return response
				else:
					form.save()
					nueva_bitacora=Bitacora(
						usuario=str(request.user.nombre),
						accion='Actualizó un historial de empleado'
						)
					nueva_bitacora.save()
					mensaje=f'{self.model.__name__} Editado Correctamente!'
					error='No hay errores!'
					response=JsonResponse({'mensaje':mensaje,'error':error})
					response.status_code=201
					return response
			else:
				mensaje=f'{self.model.__name__} no se puede registrar!'
				error=form.errors
				response=JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code=400
				return response
		else:
			return redirect('personal:inicio_historial_personal')

class EliminarHistorial(ValidarPermisosRequeridosMixin,DeleteView):
	model=HistorialPersonal
	template_name='historial_personal/eliminar_historial.html'

	def get_context_data(self,**kwargs):
		context={}
		context['HistorialPersonal']=self.get_object()
		return context

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name, self.get_context_data())

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			historial=self.get_object()
			historial.delete()
			nueva_bitacora=Bitacora(
				usuario=str(request.user.nombre),
				accion='Eliminó un historial de empleado'
			)
			nueva_bitacora.save()
			mensaje=f'{self.model.__name__} Eliminado Correctamente!'
			error='No hay errores!'
			response=JsonResponse({'mensaje':mensaje,'error':error})
			response.status_code=201
			return response
		else:
			return redirect('personal:inicio_historial_personal')

class ReporteAsistencia(TemplateView):
	template_name='bitacora/reporte_asistencia.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args,**kwargs):
		return super().dispatch(request, *args,**kwargs)

	def post(self,request, *args, **kwargs):
		ci_empleado=request.POST.get("empleado")
		fecha=request.POST.get("date_range")
		if request.POST.get("date_range")!='' and request.POST.get("empleado")=='':
			ci_empleado=request.POST.get("empleado")
			fecha=request.POST.get("date_range")
			fecha_i=datetime.datetime.strptime(fecha[0:10], "%Y-%m-%d").date()
			fecha_f=datetime.datetime.strptime(fecha[13:], "%Y-%m-%d").date()
			consulta=RegistroDeAsistencia.objects.filter(fecha_entrada__range=[fecha_i,fecha_f])
			if consulta.exists():
				""" -------------Con esto, tu haces un reporte pdf-----------"""
				template= get_template('bitacora/invoice2.html')
				context={
					'reporte': consulta,
					'comp':{'name':'Funeraria La Fé, C.A','dir':'Calle La Vigia, Valle de la Pascua 2350, Guárico','telf':'0235-3424234','ruc':'99999999','fecha_inicial':fecha_i, 'fecha_final':fecha_f}
				}
				html=template.render(context)
				css_url=os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
				pdf= HTML(string=html).write_pdf(target=f'reportes/Reporte de Asistencia de general de {fecha_i} hasta {fecha_f}.pdf',stylesheets=[CSS(css_url)])
				messages.success(request,'El reporte ha sido generado con éxito!')
				return HttpResponse(pdf, content_type='aplication/pdf')
				""" --------------------------------------------------------"""

			else:
				return render(request,'bitacora/reporte_asistencia.html', {'error':'No existen datos almacenados con estos parámetros.'})
		if request.POST.get("date_range")!='' and request.POST.get("empleado")!='':
			ci_empleado=request.POST.get("empleado")
			fecha=request.POST.get("date_range")
			fecha_i=datetime.datetime.strptime(fecha[0:10], "%Y-%m-%d").date()
			fecha_f=datetime.datetime.strptime(fecha[13:], "%Y-%m-%d").date()
			consulta=RegistroDeAsistencia.objects.filter(fecha_entrada__range=[fecha_i,fecha_f], empleado__cedula=ci_empleado)
			if consulta.exists():
				template= get_template('bitacora/invoice.html')
				context={
					'reporte': consulta,
					'comp':{'name':'Funeraria La Fé, C.A','dir':'Calle La Vigia, Valle de la Pascua 2350, Guárico','telf':'0235-3424234','ruc':'99999999','fecha_inicial':fecha_i, 'fecha_final':fecha_f}
				}
				html=template.render(context)
				css_url=os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
				pdf= HTML(string=html).write_pdf(target=f'reportes/Reporte de Asistencia de CI {ci_empleado} de {fecha_i} hasta {fecha_f}.pdf',stylesheets=[CSS(css_url)])
				messages.success(request,'El reporte ha sido generado con éxito!')
				return HttpResponse(pdf, content_type='aplication/pdf')
			else:
				return render(request,'bitacora/reporte_asistencia.html', {'error':'No existen datos almacenados con estos parámetros.'})
		return render(request,'bitacora/reporte_asistencia.html', {'error':'algo ha pasado'})

	def get(self,request,*args,**kwargs):
		try:
			if request.GET.get("date_range")!='' and request.GET.get("empleado")=='':
				ci_empleado=request.GET.get("empleado")
				fecha=request.GET.get("date_range")
				fecha_i=datetime.datetime.strptime(fecha[0:10], "%Y-%m-%d").date()
				fecha_f=datetime.datetime.strptime(fecha[13:], "%Y-%m-%d").date()
				consulta=RegistroDeAsistencia.objects.filter(fecha_entrada__range=[fecha_i,fecha_f])
				if consulta.exists():
					return render(request,'bitacora/reporte_asistencia.html', {'asistencias':consulta})
				else:
					return render(request,'bitacora/reporte_asistencia.html', {'error':'No existen datos almacenados con estos parámetros.'})
			if request.GET.get("date_range")!='' and request.GET.get("empleado")!='':
				ci_empleado=request.GET.get("empleado")
				fecha=request.GET.get("date_range")
				fecha_i=datetime.datetime.strptime(fecha[0:10], "%Y-%m-%d").date()
				fecha_f=datetime.datetime.strptime(fecha[13:], "%Y-%m-%d").date()
				consulta=RegistroDeAsistencia.objects.filter(fecha_entrada__range=[fecha_i,fecha_f], empleado__cedula=ci_empleado)
				if consulta.exists():
					return render(request,'bitacora/reporte_asistencia.html', {'asistencias':consulta})
				else:
					return render(request,'bitacora/reporte_asistencia.html', {'error':'No existen datos almacenados con estos parámetros.'})
			return render(request,'bitacora/reporte_asistencia.html')
		except:
			return render(request,'bitacora/reporte_asistencia.html')
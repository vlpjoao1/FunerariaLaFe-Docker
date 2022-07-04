from django import forms
from django.forms import Form
from .models import Personal, RegistroDeAsistencia, HistorialPersonal
import datetime
from time import gmtime, strftime

class ReporteForm(forms.Form):
	empleado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese CI del empleado', 'required':'false'}))

	date_range = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		'autocomplete':'off'
	}))




class FormularioPersonal(forms.ModelForm):
	class Meta:
		model=Personal
		fields=('cedula','nombres','apellidos','direccion','telefono','fecha_de_ingreso','foto')
		labels={
			'cedula':'Cedula (Max. 11 numeros):',
			'nombres':'Nombres:',
			'apellidos':'Apellidos:',
			'direccion':'Dirección:',
			'telefono':'Teléfono (Min. 11 números. Max. 15 números):',
			'fecha_de_ingreso':'Fecha de ingreso:',
			'foto':'Foto:'		
		}
		widgets={
			'cedula':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Cédula del empleado',
					'pattern':'[0-9]{1,14}'
				}
			),
			'nombres':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Nombres del empleado'
				}
			),
			'apellidos':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Apellidos del empleado'
				}
			),
			'direccion':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Dirección del empleado'
				}
			),
			'telefono':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Teléfono del empleado',
					'pattern':'[0-9]{11,14}'
				}
			),
			'fecha_de_ingreso':forms.SelectDateWidget(
				years=range(2000, 2030),
				attrs={
					'class':'form-control'
				}
			)
		}

		



class FormularioBitacora(forms.ModelForm):
	class Meta:
		hora=datetime.datetime.now().strftime('%H:%M')
		fecha=datetime.datetime.now().strftime('%d/%m/%Y')
		model=RegistroDeAsistencia
		fields=('empleado','si_trabajo','hora_entrada','fecha_entrada','hora_salida','fecha_salida')
		labels={'empleado':'Empleado:',
			'si_trabajo':'¿Asistió?',
			'hora_entrada':f'Hora de entrada: {hora} ',
			'fecha_entrada':'Fecha de entrada',
			'hora_salida':f'Hora de salida: {hora}',
			'fecha_salida':f'Fecha de Salida {fecha}',
		}
		widgets={
			'empleado':forms.Select(
				 attrs={
				 'class':'form-control'
				}
			),
			'si_trabajo':forms.Select(
				attrs={
				'class':'form-control',
				}
			),
			'hora_entrada':forms.TextInput(
				attrs={
				'class':'form-control',
				'placeholder':'HH:MM'
				}
			),
			'fecha_entrada':forms.SelectDateWidget(
				attrs={
				'class':'form-control'
				}
			),
			'hora_salida':forms.TextInput(
				attrs={
				'class':'form-control',
				'placeholder':'HH:MM'
				}
			),
			'fecha_salida':forms.SelectDateWidget(
				attrs={
				'class':'form-control'
				}
			),
		}

class FormularioHistorial(forms.ModelForm):
	class Meta:
		model=HistorialPersonal
		fields=('historial_empleado','acotacion','fecha_acotacion')
		labels={
			'historial_empleado':'Empleado:',
			'acotacion':'Acotación del empleado:',
			'fecha_acotacion':'Fecha:'
		}
		widgets={
			'historial_empleado':forms.Select(
				attrs={
					'class':'form-control'
				}
			),
			'acotacion':forms.Textarea(
				attrs={
					'class':'form-control'
				}
			),
			'fecha_acotacion':forms.SelectDateWidget(
				years=range(2000, 2030),
				attrs={
					'class':'form-control'
				}
			)
		}
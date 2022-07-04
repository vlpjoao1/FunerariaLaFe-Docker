from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

class FormularioLogin(AuthenticationForm):
	def __init__(self,*args,**kwargs):
		super(FormularioLogin,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs['class']='form-control'
		self.fields['username'].widget.attrs['placeholder']='Nombre de usuario'
		self.fields['password'].widget.attrs['class']='form-control'
		self.fields['password'].widget.attrs['placeholder']='Contraseña de usuario'

class FormularioUsuario(forms.ModelForm):
		""" lo hacemos de esta forma porque queremos defini un campo extra al registraru n usuario"""

		password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'placeholder':'Ingrese su contraseña',
				'id':'password1',
				'required':'required'
			}
		))
		password2=forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'placeholder':'Ingrese su contraseña',
				'id':'password2',
				'required':'required'
			}
		))
		class Meta:
			model=Usuario
			fields=('username','email','nombre','apellidos','pregunta','respuesta','is_superuser','user_permissions')
			labels={
			'username':'Username:',
			'email':'Email del usuario:',
			'nombre':'Nombres del usuario:',
			'apellidos':'Apellidos:',
			'pregunta':'Pregunta de seguridad',
			'respuesta':'Respuesta de seguridad',
			'is_superuser':'¿Será usuario administrador?',
			'user_permissions':'Permisos del usuario'
		}
			widgets={
				'username':forms.TextInput(
					attrs={
						'class':'form-control',
						'placeholder':'Ingrese username'
					}
				),
				'email':forms.TextInput(
					attrs={
						'class':'form-control',
						'placeholder':'Ingrese el correo'
					}
				),
				'nombre':forms.TextInput(
					attrs={
						'class':'form-control',
						'placeholder':'Ingrese los Nombres'
					}
				),
				'apellidos':forms.TextInput(
					attrs={
						'class':'form-control',
						'placeholder':'Ingrese los Apellidos'
					}
				),
				'pregunta':forms.Select(
					attrs={
						'class':'form-control'
					}
				),
				'respuesta':forms.TextInput(
					attrs={
						'class':'form-control',
						'placeholder':'Ingrese su respuesta de seguridad'
					}
				),	
				'user_permissions':forms.SelectMultiple(
					attrs={
						'class':'form-control'
					}
				),	
				
			}


		def clean_password2(self):
			password1=self.cleaned_data.get('password1')
			password2=self.cleaned_data.get('password2')
			if password1 != password2:
				raise forms.ValidationError('Las contraseñas no coinciden')
			return password2

		def save(self, commit=True):
			user=super().save(commit=False)
			user.set_password(self.cleaned_data['password1'])
			if commit:
				user.save()
			return user

class ResetPasswordForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Ingrese el username',
		'class':'form-control'
	}))

	choices_pregunta=[("Ciudad de nacimiento de tu madre?", "Ciudad de nacimiento de tu madre?"), ("Profesión de tu abuelo?", "Profesión de tu abuelo?"),
	("Marca de coches favorita?","Marca de coches favorita?"), ("Nombre de tu mejor amigo?","Nombre de tu mejor amigo?"),
	("Ciudad de nacimiento de tu padre?","Ciudad de nacimiento de tu padre?")]

	pregunta=forms.ChoiceField(label="Pregunta de seguridad:",choices=choices_pregunta, widget=forms.Select(attrs={'class':'form-control'}))

	respuesta = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'Ingrese la respuesta',
			'class':'form-control'
		}))
	password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'placeholder':'Ingrese su contraseña',
				'id':'password1',
				'required':'required'
			}
		))
	password2=forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'placeholder':'Ingrese su contraseña',
				'id':'password2',
				'required':'required'
			}
		))
	def clean_password2(self):
		password1=self.cleaned_data.get('password1')
		password2=self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Las contraseñas no coinciden')
		return password2

	def clean(self):
		cleaned= super().clean()
		if not Usuario.objects.filter(username=cleaned['username']).exists():
			#con esto, modificamos el mensaje de error para que diga lo que nosotros queremos
			self._errors['error']=self._errors.get('error',self.error_class())
			usuario=cleaned['username']
			self._errors['error'].append(f'El usuario {usuario} no existe')
		return cleaned

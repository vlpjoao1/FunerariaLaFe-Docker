from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ckeditor.fields import RichTextField
# Create your models here.

class UsuarioManager(BaseUserManager):
	def _create_user(self,username,email,nombre,password,is_staff, is_superuser,**extra_fields):
		user=self.model(
			username=username,
			email=email,
			nombre=nombre,
			is_staff=True,
			is_superuser=True,
			**extra_fields
			)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self,username,email,nombre,password=None, **extra_fields):
		return self._create_user(username,email,nombre,password,True, True, **extra_fields)

	def create_superuser(self,username,email,nombre,password=None, **extra_fields):
		return self._create_user(username,email,nombre,password,True, True, **extra_fields)
		

pregunta_choices=[("Ciudad de nacimiento de tu madre?", "Ciudad de nacimiento de tu madre?"), ("Profesión de tu abuelo?", "Profesión de tu abuelo?"),
	("Marca de coches favorita?","Marca de coches favorita?"), ("Nombre de tu mejor amigo?","Nombre de tu mejor amigo?"),
	("Ciudad de nacimiento de tu padre?","Ciudad de nacimiento de tu padre?")]

class Usuario(AbstractBaseUser, PermissionsMixin):
	username = models.CharField('Username', unique=True,max_length=100)
	email = models.EmailField('Email', unique=True,max_length=254)
	nombre = models.CharField('Nombres del usuario', max_length=100, blank=False, null=False)
	apellidos = models.CharField('apellidos del usuario', max_length=100, blank=False, null=False)
	imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/',max_length=255, height_field=None, width_field=None, null=True, blank=True)
	pregunta=models.CharField('Pregunta de seguridad', max_length=255, blank=False, null=True, choices=pregunta_choices)
	respuesta=models.CharField('Respuesta de seguridad', max_length=255, blank=False, null=True)
	is_active = models.BooleanField(default=True)
	is_superuser=models.BooleanField(default=True)
	is_staff = models.BooleanField(default=True)
	objects=UsuarioManager()

	USERNAME_FIELD='username'

	REQUIRED_FIELDS=['email','nombre','apellidos','pregunta','respuesta']

	def get_absolute_url(self):
		return f'/Users/Resetear/{self.username}/'

class Bitacora(models.Model):
	id=models.AutoField(primary_key=True)
	usuario=models.CharField(max_length=255, null=False, blank=False)
	accion=models.CharField(null=False, blank=False, max_length=255)
	fecha_accion=models.DateField(auto_now=True, auto_now_add=False)

	class Meta:
		verbose_name='Bitacora'
		verbose_name_plural='Bitacora'
		ordering=['fecha_accion']

	def __str__(self):
		return f'El usuario {self.usuario}, {self.accion}, la fecha: {self.fecha_accion} '

class Inicio(models.Model):
	id=models.AutoField(primary_key=True)
	contenido=RichTextField()

	class Meta:
		verbose_name='Contenido'
		verbose_name_plural='Contenidos'
		ordering=['id']
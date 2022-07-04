from django.db import models

# Create your models here.

class Personal(models.Model):
	id=models.AutoField(primary_key=True)
	cedula=models.CharField(max_length=13, blank=False, null=False, unique=True)
	nombres=models.CharField('Nombres', max_length=100, blank=False, null=False)
	apellidos=models.CharField('Apellidos',max_length=100, blank=False, null=False)
	direccion=models.CharField('Dirección', max_length=255, blank=True, null=True)
	telefono=models.CharField('Teléfono', max_length=15, null=True, blank=True)
	fecha_de_ingreso=models.DateField(blank=False, null=False)
	""" En la configuración ya pusimos la carpeta donde se va a subir las imagenes,
	aqui identificamos en la subcarpeta que se va a subir, si no existe, se creará"""
	foto=models.ImageField(upload_to='personal')

	class Meta:
		verbose_name='Empleado'
		verbose_name_plural='Empleados'
		ordering=['nombres']

	def natural_key(self):
		return f'{self.cedula}, {self.nombres} {self.apellidos}'

	def __str__(self):
		return f'{self.cedula}, {self.nombres}'

trabajo_choices=[('Si asistió','Si asistió'),('No asistió','No asistió')]

class RegistroDeAsistencia(models.Model):
	id_bitacora=models.AutoField(primary_key=True)
	empleado=models.ForeignKey(Personal, on_delete=models.CASCADE)
	si_trabajo=models.CharField(max_length=10,null=False, blank=False, choices=trabajo_choices)
	hora_entrada=models.CharField(max_length=5,blank=True, null=True)
	fecha_entrada=models.DateField(blank=True, null=True)
	hora_salida=models.CharField(max_length=5,blank=True, null=True)
	fecha_salida=models.DateField(blank=True, null=True)

	class Meta:
		verbose_name='Asistencia del Personal'
		verbose_name_plural='Asistencia del Personal'
		ordering=['hora_entrada']

	def __str__(self):
		return f'Emplado:{self.empleado}, Fecha/hora entrada: {self.hora_entrada}'


class HistorialPersonal(models.Model):
	id_historial=models.AutoField(primary_key=True)
	historial_empleado=models.ForeignKey(Personal, on_delete=models.CASCADE)
	acotacion=models.TextField(blank=False, null=False)
	fecha_acotacion=models.DateField(blank=False, null=False)

	class Meta:
		verbose_name='Historial del Personal'
		verbose_name_plural='Historial del Personal'
		ordering=['fecha_acotacion']

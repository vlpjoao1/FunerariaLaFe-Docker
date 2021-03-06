# Generated by Django 3.0.2 on 2021-02-21 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=15, unique=True)),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono')),
                ('fecha_de_ingreso', models.DateField()),
                ('foto', models.ImageField(upload_to='personal')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'ordering': ['nombres'],
            },
        ),
        migrations.CreateModel(
            name='HistorialPersonal',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('acotacion', models.TextField()),
                ('fecha_acotacion', models.DateField()),
                ('historial_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Personal')),
            ],
            options={
                'verbose_name': 'Historial del Personal',
                'verbose_name_plural': 'Historial del Personal',
                'ordering': ['fecha_acotacion'],
            },
        ),
        migrations.CreateModel(
            name='BitacoraPersonal',
            fields=[
                ('id_bitacora', models.AutoField(primary_key=True, serialize=False)),
                ('si_trabajo', models.CharField(choices=[('Si asistió', 'Si asistió'), ('No asistió', 'No asistió')], max_length=10)),
                ('hora_entrada', models.CharField(max_length=16)),
                ('fecha_entrada', models.DateField()),
                ('hora_salida', models.CharField(blank=True, max_length=16, null=True)),
                ('fecha_salida', models.DateField(blank=True, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Personal')),
            ],
            options={
                'verbose_name': 'Bitácora del Personal',
                'verbose_name_plural': 'Bitácora del Personal',
                'ordering': ['hora_entrada'],
            },
        ),
    ]

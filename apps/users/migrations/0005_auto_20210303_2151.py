# Generated by Django 3.0.2 on 2021-03-04 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210228_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]

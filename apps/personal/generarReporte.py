import os
import time
import django
from datetime import date
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ProyectoPatricia.settings")

django.setup()

from apps.personal.models import HistorialPersonal
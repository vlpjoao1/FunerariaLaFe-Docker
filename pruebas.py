from ProyectoPatricia.wsgi import *
from ProyectoPatricia import settings
from django.template.loader import get_template
from weasyprint import HTML, CSS

def printReporte():
	template=get_template('bitacora/reporte_asistencia.html')
	context= {'nombre':'Joao Goncalves'}
	html_template = template.render(context)
	css_url=os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
	HTML(string=html_template).write_pdf(target='reportes/Reporte de Asistencia.pdf', stylesheets=[CSS(css_url)])

printReporte()

FROM python:3.8
#PODER LEER LOS MENSAJES DE LA CONSOLA PYTHON
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
#carpeta de trabajo
WORKDIR /code

#copy <from> <to>
COPY requirements.txt /code/

RUN python -m pip install -r requirements.txt

#copy <local_path> to <container_path>
COPY . /code/

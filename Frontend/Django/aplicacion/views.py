# views.py
from django.shortcuts import render
from .models import Modelo

def lista_de_datos(request):
    datos = Modelo.objects.all()

    for dato in datos:
        dato.adjuntos = dato.adjuntos.split(", ")

    return render(request, 'aplicacion/lista_de_datos.html', {'datos': datos})


# views.py
from django.http import HttpResponse

def descargar_commit(request, cve):
    # Obtengo primero el commit_mensaje para el CVE específico
    commit_mensaje = Modelo.objects.get(cve=cve).commit_mensaje

    # Creo la respuesta HTTP con el contenido del commit_mensaje
    response = HttpResponse(commit_mensaje, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{cve}_commit.txt"'

    return response

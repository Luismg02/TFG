# models.py
from django.db import models

class Modelo(models.Model):
    tipo = models.TextField()
    cve = models.TextField(primary_key=True)
    commit_mensaje = models.TextField()
    adjuntos = models.TextField()
    hardware = models.TextField()
    url = models.TextField()

    #def __str__(self):
    #    return f'Tipo: {self.tipo}, CVE: {self.cve}, Mensaje: {self.commit_mensaje}, Adjuntos: {self.adjuntos}, Hardware: {self.hardware}, URL: {self.url}'

    class Meta:
        # Especifico el nombre de la tabla de la base de datos
        db_table = 'bugs'

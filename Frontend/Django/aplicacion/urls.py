# urls.py
from django.urls import path
from .views import lista_de_datos, descargar_commit

urlpatterns = [
    path('datos/', lista_de_datos, name='lista_de_datos'),
    path('descargar_commit/<str:cve>/', descargar_commit, name='descargar_commit'),
]

from django.urls import path
from contenido import views

urlpatterns = [
    path('indicadores/',views.indicadores_list,name='indicadores_list'),
]
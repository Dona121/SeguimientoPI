from django.urls import path
from proyectos import views

urlpatterns = [
    path('agregar_proyectos/<int:id_meta>/',views.proyectos_pdd,name='agregar_proyecto'),
    path('editar_proyecto/<int:id_proyecto>/',views.proyectos_pdd,name='editar_proyecto'),
]
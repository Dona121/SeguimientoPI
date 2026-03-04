from django.shortcuts import render
from contenido import models

# Create your views here.

def indicadores_list(request):
    indicadores = models.IndicadorMGA.objects.prefetch_related('proyectos_set').all()
    return render(
        request,
        'metas.html',
        {'indicadores':indicadores}
    )
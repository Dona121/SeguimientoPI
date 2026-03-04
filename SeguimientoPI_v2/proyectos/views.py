from django.shortcuts import render, redirect, get_object_or_404
from proyectos.models import Proyectos
from proyectos.forms import ProyectosForm

# Create your views here.

def proyectos_pdd(request, id_proyecto=0,id_meta=0):
    if request.method == "GET":
        if id_proyecto != 0:
            proyecto = get_object_or_404(
                Proyectos,
                id=id_proyecto
            )
            form = ProyectosForm(instance=proyecto)
        else:
            form = ProyectosForm(initial={'meta':id_meta})
    else:
        if id_proyecto != 0:
            proyecto = get_object_or_404(
                Proyectos,
                id=id_proyecto
            )
            form = ProyectosForm(request.POST,instance=proyecto)
        else:
            form = ProyectosForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('indicadores_list')

    return render(  
        request,
        'proyectos.html',
        {'form':form}
    )

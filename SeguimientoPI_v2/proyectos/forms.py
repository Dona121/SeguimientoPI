from django import forms
from proyectos.models import Programaciones, Proyectos


class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = '__all__'
        widgets = {
            'nombre_proyecto': forms.Textarea(attrs={'class':'nombre-proyecto'})
        }


class ProgramacionesForm(forms.ModelForm):
    class Meta:
        model = Programaciones
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.reporte_editable():
            self.fields['programacion'].disable = True
            self.fields['ejecucion'].disable = True
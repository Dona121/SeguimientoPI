from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from proyectos import models
from proyectos.forms import ProgramacionesForm

# Register your models here.

@admin.register(models.Vigencias)
class VigenciasAdmin(admin.ModelAdmin):
    list_display = ('vigencia',)

@admin.register(models.Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('municipio',)
    list_filter = ('municipio',)

@admin.register(models.Meses)
class MesesAdmin(admin.ModelAdmin):
    list_display = ('mes',)


@admin.register(models.TiposDeBanco)
class TiposDeBancoAdmin(ModelAdmin):
    list_display = ('tipo_banco',)

class ProgramacionInline(TabularInline):
    model = models.Programaciones
    form = ProgramacionesForm
    tab = True
    extra = 1


@admin.register(models.Fuentes)
class FuentesAdmin(ModelAdmin):
    list_display = ("codigo_fuente_financiacion","fuente_financiacion",)

class FuentesInline(TabularInline):
    model = models.FuentesFinanciacion
    fields = ('fuente_financiacion','valor')
    tab  = True
    extra = 1

@admin.register(models.Proyectos)
class ProyectosAdmin(ModelAdmin):
    list_display = ('meta','bpin','nombre_proyecto')
    filter_horizontal = ('tipo_de_banco','municipios')
    inlines = (ProgramacionInline,FuentesInline) # Una forma de entender esto puede ser: Oye django, para este proyecto quiero crear un formulario
    # de programaciones, como el ID del proyecto al seleccionarlo es uno y no cambia, cada que que se agrege un formulario de programaciones
    # cada uno de los registro de programaciones va a tomar el ID del proyecto, dandole logica a la relaciones. Varias vigencias pueden tener
    # un mismo proyecto

# El inline lo hago desde programaciones porque desde ahi es que quiero crear un formulario. Agregando la vigencia y el proyecto asociado
# Para cada vigencia el mismo proyecto
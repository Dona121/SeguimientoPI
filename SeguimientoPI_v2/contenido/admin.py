from django.contrib import admin
from django.contrib.admin import AdminSite
from contenido import models
from unfold.admin import TabularInline
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from django.template.defaultfilters import truncatechars
from proyectos.models import Proyectos
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

# Register your models here.

@admin.register(models.LineaEstrategica)
class LineaEstrategicaAdmin(UnfoldModelAdmin):
    list_display = ("linea_estrategica",)

@admin.register(models.SectorPDD)
class SectorPDDAdmin(UnfoldModelAdmin):
    list_display = ("sector_pdd",)
    raw_id_fields = ('linea_estrategica',)

@admin.register(models.ProgramaPDD)
class ProgramaPDDAdmin(UnfoldModelAdmin):
    list_display = ("programa_pdd",)
    raw_id_fields = ('sector_pdd',)

@admin.register(models.SectorMGA)
class SectorMGAAdmin(UnfoldModelAdmin):
    list_display = ("sector_mga","codigo_sector_mga")
    filter_horizontal = ('programa_pdd',)

@admin.register(models.ProgramaMGA)
class ProgramaMGAdmin(UnfoldModelAdmin):
    list_display = ("programa_mga","codigo_programa_mga")

@admin.register(models.ProductoMGA)
class ProductoMGAdmin(UnfoldModelAdmin):
    list_display = ("producto_mga","codigo_producto_mga")
    raw_id_fields = ('programa_mga',)

@admin.register(models.UnidadMedida)
class UnidadMedida(UnfoldModelAdmin):
    list_display = ("unidad_medida",)

@admin.register(models.Dependencias)
class DependenciasAdmin(UnfoldModelAdmin):
    list_display = ("dependencia","correo")

@admin.register(models.IndicadorMGA)
class IndicadorMGAAdmin(UnfoldModelAdmin):
    list_display = ("producto_mga","indicador_mga","codigo_indicador_mga",
                    "descripcion_indicador","medido_a_traves_de","medido_a_traves_de",
                    "tiene_edt","unidad_medida","tipo_de_acumulacion",
                    "meta_cuatrienio","meta_fisica_esperada_2024","meta_fisica_esperada_2025","meta_fisica_esperada_2026",
                    "meta_fisica_esperada_2027","proyectos")
    raw_id_fields = ('producto_mga',)

    def descripcion_indicador(self,obj):
        return truncatechars(obj.descripcion,20)
    
    def proyectos(self,obj):
        proyectos = obj.proyectos_set.all()
        url_admin = reverse("admin:proyectos_proyectos_changelist")
        parametro_consulta = "?id="
        urls = []
        for proyecto in proyectos:
            consulta = parametro_consulta+str(proyecto.id)
            # parametro_consulta = f"?id={proyecto.id}"
            url_proyecto = format_html("<a href='{}{}'>{}</a>",url_admin,consulta,proyecto.bpin)
            urls.append(url_proyecto)
        return mark_safe(", ".join(urls))

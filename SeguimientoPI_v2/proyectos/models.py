from django.db import models
from django.core.exceptions import ValidationError
from contenido.models import SectorMGA, IndicadorMGA
from django.utils import timezone

# Create your models here.

class TiposDeBanco(models.Model):
    tipo_banco = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Banco'
        verbose_name_plural = 'Tipos de Banco'

    def __str__(self):
        return f"{self.tipo_banco}"

class Municipios(models.Model):
    municipio = models.CharField(max_length=30)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        constraints = [
            models.UniqueConstraint(fields=('municipio',),name='municipio_unique')
        ]

    def __str__(self):
        return f"{self.municipio}"

class Proyectos(models.Model):
    bpin = models.CharField(max_length=20)
    nombre_proyecto = models.TextField()
    tipo_de_banco = models.ManyToManyField(
        TiposDeBanco
    )
    meta = models.ForeignKey(
        IndicadorMGA,
        on_delete=models.CASCADE,
        blank=False,
        null=True
    )
    municipios = models.ManyToManyField(
        Municipios,
        blank=False,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
    
    def __str__(self):
        return f"{self.bpin}"
    
class Vigencias(models.Model):
    vigencia = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vigecia'
        verbose_name_plural = 'Vigencias'

    def __str__(self):
        return f"{self.vigencia}"
    
class Meses(models.Model):
    mes = models.CharField(max_length=20)
    numero = models.PositiveSmallIntegerField(blank=False,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mes'
        verbose_name_plural = 'Meses'

    def __str__(self):
        return f"{self.mes}"

class Programaciones(models.Model):
    vigencia = models.ForeignKey(
        Vigencias,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    mes = models.ForeignKey(
        Meses,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    programacion = models.DecimalField(max_digits=30,decimal_places=10)
    ejecucion = models.DecimalField(max_digits=30,decimal_places=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    proyectos = models.ForeignKey(
        Proyectos,
        on_delete=models.CASCADE,
        blank=False,
        null=True
    ) # A un a vigencia puedo asociar un proyecto, si creo otra vigencia, le puedo asociar el mismo prouyecto
    # Por ejemplo: 2024 - Proyecto 1, 2025 - Proyecto 1

    class Meta:
        verbose_name = 'Programacion'
        verbose_name_plural = 'Programaciones'
        constraints = [
            models.UniqueConstraint(fields=('vigencia','mes',"proyectos"),name='unique_vigencia_mes')
        ]

    def __str__(self):
        return f"{self.vigencia}"
    
    def reporte_editable(self):
        hoy = timezone.localdate()
        return (self.vigencia == hoy.year and self.mes.numero == hoy.month)
    
class Fuentes(models.Model):
    codigo_fuente_financiacion = models.CharField(max_length=30)
    fuente_financiacion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fuente de Finanacion'
        verbose_name_plural = 'Fuentes de Financiacion'
        constraints = [
            models.UniqueConstraint(fields=('codigo_fuente_financiacion','fuente_financiacion'),name='codigo_fuente_nombre_fuente')
        ]
    def __str__(self):
        return f"{self.fuente_financiacion}"
    
class FuentesFinanciacion(models.Model):
    fuente_financiacion = models.ForeignKey(
        Fuentes,
        on_delete=models.CASCADE
    )
    vigencia = models.ForeignKey(
        Vigencias,
        on_delete=models.CASCADE,
        blank=False,
        null=True
    )
    valor = models.DecimalField(max_digits=30,decimal_places=10,blank=False,null=True)
    sector_mga = models.ManyToManyField(
        SectorMGA,
        blank=False,
        null=True
    )
    proyectos = models.ForeignKey(
        Proyectos,
        on_delete=models.CASCADE,
        blank=False,
        null=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fuente de Finanacion'
        verbose_name_plural = 'Fuentes de Financiacion'
        constraints = [
            models.UniqueConstraint(fields=('fuente_financiacion','vigencia'),name='fuente_vigencia')
        ]
    def __str__(self):
        return f"{self.fuente_financiacion}"
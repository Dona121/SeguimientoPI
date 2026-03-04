from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class TipoAcumulacion(models.TextChoices):
    ACUMULATIVO = 'AC'
    NO_ACUMULATIVO = 'NC'

class LineaEstrategica(models.Model):
    linea_estrategica = models.CharField(max_length=80)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Linea Estrategica'
        verbose_name_plural = 'Lineas Estrategicas'
    
    def __str__(self):
        return f"{self.linea_estrategica}"
    
class SectorPDD(models.Model):
    linea_estrategica = models.ForeignKey(
        LineaEstrategica,
        on_delete=models.CASCADE
    )
    sector_pdd = models.CharField(max_length=80)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Sector PDD'
        verbose_name_plural = 'Sectores PDD'
    
    def __str__(self):
        return f"{self.sector_pdd}"
    
class ProgramaPDD(models.Model):
    sector_pdd = models.ForeignKey(
        SectorPDD,
        on_delete=models.CASCADE
    )
    programa_pdd = models.CharField(max_length=80)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Programa PDD'
        verbose_name_plural = 'Programas PDD'
    
    def __str__(self):
        return f"{self.programa_pdd}"
    
    
class SectorMGA(models.Model):
    programa_pdd = models.ManyToManyField(
        ProgramaPDD
    )
    sector_mga = models.CharField(max_length=80)
    codigo_sector_mga = models.CharField(max_length=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Sector MGA'
        verbose_name_plural = 'Sectores MGA'
    
    def __str__(self):
        return f"{self.sector_mga}"
    
class ProgramaMGA(models.Model):
    sector_mga = models.ForeignKey(
        SectorMGA,
        on_delete=models.CASCADE
    )
    programa_mga = models.CharField(max_length=80)
    codigo_programa_mga = models.CharField(max_length=4)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Programa MGA'
        verbose_name_plural = 'Programas MGA'
    
    def __str__(self):
        return f"{self.programa_mga}"


class ProductoMGA(models.Model):
    programa_mga = models.ForeignKey(
        ProgramaMGA,
        on_delete=models.CASCADE
    )
    producto_mga = models.CharField(max_length=80)
    codigo_producto_mga = models.CharField(max_length=7)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Producto MGA'
        verbose_name_plural = 'Productos MGA'
    
    def __str__(self):
        return f"{self.producto_mga}"
    

class UnidadMedida(models.Model):
    unidad_medida = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
    
    def __str__(self):
        return f'{self.unidad_medida}'
    
class Dependencias(models.Model):
    dependencia = models.CharField(max_length=150)
    correo = models.EmailField(blank=True,null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'
    
    def __str__(self):
        return f"{self.dependencia}"

class IndicadorMGA(models.Model):
    producto_mga = models.ForeignKey(
        ProductoMGA,
        on_delete=models.CASCADE
    )
    indicador_mga = models.CharField(max_length=80)
    codigo_indicador_mga = models.CharField(max_length=9)
    descripcion = models.TextField()
    medido_a_traves_de = models.CharField(max_length=100)
    tiene_edt = models.BooleanField()
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.CASCADE
    )
    tipo_de_acumulacion = models.CharField(max_length=2,choices=TipoAcumulacion.choices)
    dependencia_responsable = models.ManyToManyField(
        Dependencias
    )
    meta_cuatrienio = models.DecimalField(max_digits=30,decimal_places=10)
    meta_fisica_esperada_2024 = models.DecimalField(max_digits=30,decimal_places=10)
    meta_fisica_esperada_2025 = models.DecimalField(max_digits=30,decimal_places=10)
    meta_fisica_esperada_2026 = models.DecimalField(max_digits=30,decimal_places=10)
    meta_fisica_esperada_2027 = models.DecimalField(max_digits=30,decimal_places=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_creacion'])
        ]
        verbose_name = 'Indicador MGA'
        verbose_name_plural = 'Indicadores MGA'
    
    def __str__(self):
        return f"{self.producto_mga}"
    
    def clean(self):
        if self.tipo_de_acumulacion == TipoAcumulacion.ACUMULATIVO:
            if not sum([self.meta_fisica_esperada_2024,\
                    self.meta_fisica_esperada_2025,\
                    self.meta_fisica_esperada_2026],\
                    self.meta_fisica_esperada_2027
                ) == self.meta_cuatrienio:
                raise ValidationError("Cuando el tipo de acumulación es acumulativo, la suma de la programación de las cuatro\
                                      vigencias debe ser igual a la meta del cuatrienio")
        if self.tipo_de_acumulacion == TipoAcumulacion.NO_ACUMULATIVO:
            if not (sum([self.meta_fisica_esperada_2024,\
                    self.meta_fisica_esperada_2025,\
                    self.meta_fisica_esperada_2026],\
                    self.meta_fisica_esperada_2027
                )/4) == self.meta_cuatrienio:
                raise ValidationError("Cuando el tipo de acumulación es no acumulativo, el promedio de la programación de las cuatro\
                                      vigencias debe ser igual a la meta del cuatrienio")
        super().clean()
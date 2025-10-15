from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

# Create your models here.
class Apartado(models.Model):
    cantidad_cuotas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    cuotas_pendientes = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    estado = models.ForeignKey(
        "dominios_comunes.Estado", 
        on_delete=models.RESTRICT
    )
    fecha_limite = models.DateField()

    def __str__(self):
        return f"Apartado - Cuotas: {self.cuotas_pendientes}/{self.cantidad_cuotas}"

    def clean(self):
        if self.cuotas_pendientes > self.cantidad_cuotas:
            raise ValidationError("Las cuotas pendientes no pueden ser mayores que el total de cuotas")

    def esta_vencido(self):
        """Verifica si el apartado está vencido"""
        return self.fecha_limite < timezone.now().date()

    def porcentaje_pagado(self):
        """Calcula el porcentaje pagado del apartado"""
        cuotas_pagadas = self.cantidad_cuotas - self.cuotas_pendientes
        return (cuotas_pagadas / self.cantidad_cuotas) * 100 if self.cantidad_cuotas > 0 else 0

    class Meta:
        verbose_name = "Apartado"
        verbose_name_plural = "Apartados"
        constraints = [
            models.CheckConstraint(
                check=models.Q(cuotas_pendientes__lte=models.F('cantidad_cuotas')),
                name='apartado_cuotas_pendientes_validas'
            ),
        ]

class Credito(models.Model):
    cantidad_cuotas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    cuotas_pendientes = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    interes = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))]
    )
    estado = models.ForeignKey(
        "dominios_comunes.Estado", 
        on_delete=models.RESTRICT
    )
    fecha_limite = models.DateField()

    def __str__(self):
        return f"Crédito - Cuotas: {self.cuotas_pendientes}/{self.cantidad_cuotas} - Interés: {self.interes}%"

    def clean(self):
        if self.cuotas_pendientes > self.cantidad_cuotas:
            raise ValidationError("Las cuotas pendientes no pueden ser mayores que el total de cuotas")

    def esta_vencido(self):
        """Verifica si el crédito está vencido"""
        return self.fecha_limite < timezone.now().date()

    def porcentaje_pagado(self):
        """Calcula el porcentaje pagado del crédito"""
        cuotas_pagadas = self.cantidad_cuotas - self.cuotas_pendientes
        return (cuotas_pagadas / self.cantidad_cuotas) * 100 if self.cantidad_cuotas > 0 else 0

    class Meta:
        verbose_name = "Crédito"
        verbose_name_plural = "Créditos"
        constraints = [
            models.CheckConstraint(
                check=models.Q(cuotas_pendientes__lte=models.F('cantidad_cuotas')),
                name='credito_cuotas_pendientes_validas'
            ),
        ]

class Cuota(models.Model):
    credito = models.ForeignKey(
        "Credito", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="cuotas"
    )
    apartado = models.ForeignKey(
        "Apartado", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="cuotas"
    )
    fecha = models.DateField()
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    metodo_pago = models.ForeignKey(
        "dominios_comunes.MetodoPago", 
        on_delete=models.RESTRICT
    )

    def __str__(self):
        if self.credito:
            return f"Cuota Crédito - ${self.monto} - {self.fecha}"
        elif self.apartado:
            return f"Cuota Apartado - ${self.monto} - {self.fecha}"
        return f"Cuota - ${self.monto} - {self.fecha}"

    def clean(self):
        # Validación XOR crítica: una cuota debe pertenecer SOLO a crédito O apartado
        if not self.credito and not self.apartado:
            raise ValidationError("La cuota debe pertenecer a un crédito o un apartado")
        
        if self.credito and self.apartado:
            raise ValidationError("La cuota no puede pertenecer tanto a un crédito como a un apartado")
        
        if self.monto <= 0:
            raise ValidationError("El monto de la cuota debe ser mayor que cero")

    def esta_vencida(self):
        """Verifica si la cuota está vencida"""
        return self.fecha < timezone.now().date()

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"
        ordering = ['-fecha']
        constraints = [
            # Constraint XOR: debe pertenecer a crédito O apartado, no ambos ni ninguno
            models.CheckConstraint(
                check=(
                    (models.Q(credito__isnull=False) & models.Q(apartado__isnull=True)) |
                    (models.Q(credito__isnull=True) & models.Q(apartado__isnull=False))
                ),
                name='cuota_credito_xor_apartado'
            ),
        ]
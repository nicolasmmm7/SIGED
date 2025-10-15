from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.
class Compra(models.Model):
    proveedor = models.ForeignKey(
        "terceros.Proveedor", 
        on_delete=models.RESTRICT,
        related_name="compras"
    )
    credito = models.ForeignKey(
        "apartado_credito.Credito", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="compras"
    )
    precio_por_gramo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    metodo_pago = models.ForeignKey(
        "dominios_comunes.MetodoPago", 
        on_delete=models.RESTRICT
    )
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f"Compra - {self.proveedor.nombre} - ${self.total}"

    def clean(self):
        if self.precio_por_gramo <= 0:
            raise ValidationError("El precio por gramo debe ser mayor que cero")
        if self.total <= 0:
            raise ValidationError("El total debe ser mayor que cero")

    def total_gramos(self):
        """Calcula el total de gramos en la compra"""
        return sum(cp.prenda.gramos * cp.cantidad for cp in self.prendas.all())

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha']

class CompraPrenda(models.Model):
    compra = models.ForeignKey(
        "Compra", 
        on_delete=models.CASCADE, 
        related_name="prendas"
    )
    prenda = models.ForeignKey(
        "prendas.Prenda", 
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.compra} - {self.prenda} (Cant: {self.cantidad})"

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero")

    def save(self, *args, **kwargs):
        # Control automático de inventario
        is_new = self.pk is None
        if is_new:
            # Nueva compra - aumentar existencia
            super().save(*args, **kwargs)
            self.prenda.existencia += self.cantidad
            self.prenda.save(update_fields=['existencia'])
        else:
            # Actualización - calcular diferencia
            old_instance = CompraPrenda.objects.get(pk=self.pk)
            super().save(*args, **kwargs)
            diferencia = self.cantidad - old_instance.cantidad
            self.prenda.existencia += diferencia
            self.prenda.save(update_fields=['existencia'])

    def delete(self, *args, **kwargs):
        # Reducir existencia al eliminar
        self.prenda.existencia -= self.cantidad
        self.prenda.save(update_fields=['existencia'])
        super().delete(*args, **kwargs)

    def subtotal_gramos(self):
        """Calcula el subtotal en gramos"""
        return self.prenda.gramos * self.cantidad

    class Meta:
        verbose_name = "Compra Prenda"
        verbose_name_plural = "Compras Prendas"
        unique_together = ['compra', 'prenda']

class Venta(models.Model):
    cliente = models.ForeignKey(
        "terceros.Cliente", 
        on_delete=models.RESTRICT,
        related_name="ventas"
    )
    credito = models.ForeignKey(
        "apartado_credito.Credito", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="ventas"
    )
    apartado = models.ForeignKey(
        "apartado_credito.Apartado", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="ventas"
    )
    precio_por_gramo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    gramo_ganancia = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))]
    )
    metodo_pago = models.ForeignKey(
        "dominios_comunes.MetodoPago", 
        on_delete=models.RESTRICT
    )
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f"Venta - {self.cliente.nombre} - ${self.total}"

    def clean(self):
        # Validación XOR crítica: una venta NO puede tener crédito Y apartado
        if self.credito and self.apartado:
            raise ValidationError("Una venta no puede tener tanto crédito como apartado al mismo tiempo")
        
        if self.precio_por_gramo <= 0:
            raise ValidationError("El precio por gramo debe ser mayor que cero")
        if self.gramo_ganancia < 0:
            raise ValidationError("La ganancia por gramo no puede ser negativa")
        if self.total <= 0:
            raise ValidationError("El total debe ser mayor que cero")

    def total_gramos(self):
        """Calcula el total de gramos en la venta"""
        return sum(vp.prenda.gramos * vp.cantidad for vp in self.prendas.all())

    def ganancia_total(self):
        """Calcula la ganancia total en la venta"""
        return self.total_gramos() * self.gramo_ganancia

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']
        constraints = [
            # Constraint XOR: no puede tener tanto crédito como apartado
            models.CheckConstraint(
                check=~(models.Q(credito__isnull=False) & models.Q(apartado__isnull=False)),
                name='venta_no_credito_y_apartado'
            ),
        ]

class VentaPrenda(models.Model):
    venta = models.ForeignKey(
        "Venta", 
        on_delete=models.CASCADE, 
        related_name="prendas"
    )
    prenda = models.ForeignKey(
        "prendas.Prenda", 
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.venta} - {self.prenda} (Cant: {self.cantidad})"

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero")
        
        # Verificar stock antes de vender
        if not self.prenda.tiene_stock(self.cantidad):
            raise ValidationError(
                f"No hay suficiente stock. Disponible: {self.prenda.existencia}, "
                f"Requerido: {self.cantidad}"
            )

    def save(self, *args, **kwargs):
        # Control automático de inventario
        is_new = self.pk is None
        if is_new:
            # Nueva venta - verificar y reducir stock
            if not self.prenda.tiene_stock(self.cantidad):
                raise ValidationError(f"No hay suficiente stock para {self.prenda}")
            super().save(*args, **kwargs)
            self.prenda.existencia -= self.cantidad
            self.prenda.save(update_fields=['existencia'])
        else:
            # Actualización - calcular diferencia
            old_instance = VentaPrenda.objects.get(pk=self.pk)
            diferencia = self.cantidad - old_instance.cantidad
            if diferencia > 0 and not self.prenda.tiene_stock(diferencia):
                raise ValidationError("No hay suficiente stock para aumentar la cantidad")
            super().save(*args, **kwargs)
            self.prenda.existencia -= diferencia
            self.prenda.save(update_fields=['existencia'])

    def delete(self, *args, **kwargs):
        # Devolver stock al eliminar venta
        self.prenda.existencia += self.cantidad
        self.prenda.save(update_fields=['existencia'])
        super().delete(*args, **kwargs)

    def subtotal_gramos(self):
        """Calcula el subtotal en gramos"""
        return self.prenda.gramos * self.cantidad

    class Meta:
        verbose_name = "Venta Prenda"
        verbose_name_plural = "Ventas Prendas"
        unique_together = ['venta', 'prenda']
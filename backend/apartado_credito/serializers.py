from rest_framework import serializers
from .models import Apartado, Credito, Cuota


class ApartadoSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Apartado
        fields = '__all__'

    def get_estado_nombre(self, obj):
        """
        Devuelve el nombre (usando __str__) del estado o None si no hay relación.
        """
        return str(obj.estado) if obj.estado else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['estado_nombre'] = self.get_estado_nombre(instance)
        return rep

    def update(self, instance, validated_data):
        """
        Permite actualizaciones parciales sin requerir todos los campos.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance


class CreditoSerializer(serializers.ModelSerializer):
    estado_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Credito
        fields = '__all__'
        extra_fields = ['estado_detalle']

    def get_estado_detalle(self, obj):
        return str(obj.estado) if obj.estado else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['estado_detalle'] = self.get_estado_detalle(instance)
        return rep

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance


class CuotaSerializer(serializers.ModelSerializer):
    # Campos descriptivos (solo lectura, se muestran en el JSON de salida)
    metodo_pago_nombre = serializers.CharField(source='metodo_pago.__str__', read_only=True)
    credito_detalle = serializers.CharField(source='credito.__str__', read_only=True)
    apartado_detalle = serializers.CharField(source='apartado.__str__', read_only=True)

    class Meta:
        model = Cuota
        # Mostramos los campos con nombres legibles
        fields = [
            'id',
            'fecha',
            'monto',
            'metodo_pago',
            'metodo_pago_nombre',  # nombre legible del método de pago
            'credito',
            'credito_detalle',     # texto legible del crédito
            'apartado',
            'apartado_detalle'     # texto legible del apartado
        ]

    def update(self, instance, validated_data):
        """Permitir actualizaciones parciales (PATCH) sin requerir todos los campos."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()  # Valida según reglas del modelo (clean)
        instance.save()
        return instance

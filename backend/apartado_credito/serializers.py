from rest_framework import serializers
from .models import Apartado, Credito, Cuota


class ApartadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartado
        fields = '__all__'

    def update(self, instance, validated_data):
        # Permitir actualizaciones parciales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()  # valida antes de guardar
        instance.save()
        return instance


class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'

    def update(self, instance, validated_data):
        # Permitir actualizaciones parciales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance


class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = '__all__'

    def update(self, instance, validated_data):
        # Permitir actualizaciones parciales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Apartado, Credito, Cuota
from .serializers import ApartadoSerializer, CreditoSerializer, CuotaSerializer


class ApartadoViewSet(viewsets.ModelViewSet):
    queryset = Apartado.objects.all()
    serializer_class = ApartadoSerializer

    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Permitir actualizaciones parciales (PATCH)"""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer

    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CuotaViewSet(viewsets.ModelViewSet):
    queryset = Cuota.objects.all()
    serializer_class = CuotaSerializer

    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

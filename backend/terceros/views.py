from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Proveedor, Cliente
from .serializers import ProveedorSerializer, ClienteSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    Vista que permite realizar operaciones CRUD sobre los proveedores.
    Soporta actualizaciones parciales mediante el método PATCH.
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def update(self, request, *args, **kwargs):
        """
        Sobrescribe el método update para soportar tanto PUT como PATCH.
        Si es una actualización parcial, solo actualiza los campos enviados.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Método explícito para PATCH — actualización parcial.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Vista que permite realizar operaciones CRUD sobre los clientes.
    Soporta actualizaciones parciales mediante el método PATCH.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def update(self, request, *args, **kwargs):
        """
        Sobrescribe el método update para soportar tanto PUT como PATCH.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Método explícito para PATCH — actualización parcial.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

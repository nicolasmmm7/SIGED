"use client";
import { useEffect, useState } from "react";
import ClientCard from "../components/ClientCard";
import ClientDetail from "../components/ClientDetail";

const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClient, setSelectedClient] = useState(null);
  const [error, setError] = useState(null);

  // 🔹 Llamada al backend al montar el componente
  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/terceros/clientes/");
        if (!response.ok) throw new Error("Error al obtener los clientes");
        const data = await response.json();
        setClientes(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchClientes();
  }, []);

  // 🔹 Mostrar u ocultar detalle del cliente (tipo acordeón)
  const handleSelect = async (cliente) => {
    // Si el cliente ya está abierto → cerrarlo
    if (selectedClient?.id === cliente.id) {
      setSelectedClient(null);
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/terceros/clientes/${cliente.id}/`);
      if (!response.ok) throw new Error("Error al obtener detalle del cliente");
      const detalle = await response.json();
      setSelectedClient(detalle);
    } catch (err) {
      console.error("Error cargando detalle:", err);
    }
  };

  const handleEdit = (id) => {
    console.log("Editar cliente con ID:", id);
  };

  const handleDelete = (id) => {
    console.log("Eliminar cliente con ID:", id);
  };

  if (loading) return <p className="text-center text-gray-500">Cargando clientes...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Clientes</h2>

      <div className="flex flex-col gap-4">
        {clientes.map((cliente) => (
          <div key={cliente.id} className="bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
            {/* Tarjeta del cliente */}
            <ClientCard
              cliente={cliente}
              isOpen={selectedClient?.id === cliente.id}
              onSelect={() => handleSelect(cliente)}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />

            {/* Detalle del cliente (solo visible si está seleccionado) */}
            {selectedClient?.id === cliente.id && (
              <div
                className="p-4 bg-white border-t border-gray-200 transition-all duration-500 ease-in-out"
              >
                <ClientDetail
                  cliente={selectedClient}
                  resumen={{
                    totalCompras: 2500000,
                    cantidadCompras: 5,
                  }}
                  historial={[
                    { id: 1, producto: "Anillo de Oro", fecha: "2025-09-20", monto: 350000 },
                    { id: 2, producto: "Pulsera de Plata", fecha: "2025-08-15", monto: 180000 },
                  ]}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Clientes;

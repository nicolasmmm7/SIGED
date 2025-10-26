"use client";
import { useEffect, useState } from "react";
import ClientCard from "../Components/ClientCard";
import ClientDetail from "../Components/ClientDetail";
// import ClientSearchBar from "../Components/ClientSearchBar"; // 🔹 Lo añadiremos más adelante

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

   // 🔹 Cuando se selecciona un cliente (clic en flecha)
  const handleSelect = async (cliente) => {
    try {
      setSelectedClient(cliente);

      const response = await fetch(`http://127.0.0.1:8000/api/terceros/clientes/${cliente.id}/`);
      if (!response.ok) throw new Error("Error al obtener detalle del cliente");
      const detalle = await response.json();
      setSelectedClient(detalle);

    } catch (err) {
      console.error("Error cargando detalle:", err);
    }
  };
  if (loading) return <p className="text-center text-gray-500">Cargando clientes...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Clientes</h2>

      {/* 🔹 Cuando tengamos la barra de búsqueda
      <ClientSearchBar onSearch={handleSearch} />
      */}

      <div className="flex flex-col gap-4">
      {clientes.map((cliente) => (
      <ClientCard
      key={cliente.id}
      cliente={cliente}
      onSelect={setSelectedClient}
    />
  ))}
</div>
{/* 🔹 Panel de detalle (solo si hay cliente seleccionado) */}
      {selectedClient && (
        <div className="mt-8 transition-all duration-300 transform scale-100 opacity-100">
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
  );
};

export default Clientes;

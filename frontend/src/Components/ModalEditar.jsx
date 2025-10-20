import React, { useState } from "react";
import "../css/Modal.css";

//VENTANA EMERGENTE PARA CUANDO SE QUIERA EDITAR ALGUNA PRENDA

export default function ModalEditar({ prenda, onClose, onSaved }) {
  const [form, setForm] = useState({
    nombre: prenda.nombre,
    existencia: prenda.existencia,
    es_chatarra: prenda.es_chatarra,
    es_recuperable: prenda.es_recuperable,
  });

  const handleSave = async () => {
    const response = await fetch(`http://127.0.0.1:8000/api/prendas/prendas/${prenda.id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    if (response.ok) {
      onSaved();
      onClose();
    } else {
      alert("Error al actualizar la prenda");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-contenido">
        <h2>Editar Prenda</h2>

        <label>Nombre</label>
        <input
          value={form.nombre}
          onChange={(e) => setForm({ ...form, nombre: e.target.value })}
        />

        <label>Cantidad</label>
        <input
          type="number"
          value={form.existencia}
          onChange={(e) => setForm({ ...form, existencia: e.target.value })}
        />

        <div className="check-grupo">
          <label>
            <input
              type="checkbox"
              checked={form.es_chatarra}
              onChange={(e) => setForm({ ...form, es_chatarra: e.target.checked })}
            />
            Chatarra
          </label>

          <label>
            <input
              type="checkbox"
              checked={form.es_recuperable}
              onChange={(e) => setForm({ ...form, es_recuperable: e.target.checked })}
            />
            Recuperable
          </label>
        </div>

        <div className="modal-botones">
          <button className="btn-cancelar" onClick={onClose}>
            Cancelar
          </button>
          <button className="btn-guardar" onClick={handleSave}>
            Guardar
          </button>
        </div>
      </div>
    </div>
  );
}

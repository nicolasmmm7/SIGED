
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AdminLayout from './layoutsAdmin/AdminLayout';
import Login from "./Pages/Login";
import Inicio from './Pages/Inicio';
import Clientes from './Pages/Clientes';
import Proveedores from './Pages/Proveedores';
import DeudasCobrar from './Pages/DeudasCobrar';
import DeudasPagar from './Pages/DeudasPagar';
import Inventario from './Pages/Inventario';
import Caja from './Pages/Caja';
import './App.css';



function App() {
  return (
    <Router>
      <Routes>
        {/* 🔹 Ruta principal redirige al login */}
        <Route path="/" element={<Login />} />

        {/* 🔹 Rutas protegidas del panel admin */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Inicio />} />
          <Route path="clientes" element={<Clientes />} />
          <Route path="proveedores" element={<Proveedores />} />
          <Route path="deudas/cobrar" element={<DeudasCobrar />} />
          <Route path="deudas/pagar" element={<DeudasPagar />} />
          <Route path="inventario" element={<Inventario />} />
          <Route path="caja" element={<Caja />} />
        </Route>

        {/* 🔹 Si la ruta no existe, redirigir al login */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AdminLayout from './layoutsAdmin/AdminLayout';
import Inicio from './pages/Inicio';
import Clientes from './pages/Clientes';
import Proveedores from './pages/Proveedores';
import DeudasCobrar from './pages/DeudasCobrar';
import DeudasPagar from './pages/DeudasPagar';
import Inventario from './pages/Inventario';
import Caja from './pages/Caja';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/admin" replace />} />
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Inicio />} />
          <Route path="clientes" element={<Clientes />} />
          <Route path="proveedores" element={<Proveedores />} />
          <Route path="deudas/cobrar" element={<DeudasCobrar />} />
          <Route path="deudas/pagar" element={<DeudasPagar />} />
          <Route path="inventario" element={<Inventario />} />
          <Route path="caja" element={<Caja />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

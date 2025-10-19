import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Pages/Login";

function Dashboard() {
  return <h1>Bienvenida Susana 💎</h1>;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
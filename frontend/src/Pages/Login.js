import React, { useState } from "react";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // importante para mantener la sesión
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      window.location.href = "/dashboard";
    } else {
      const data = await response.json();
      setError(data.error || "Error al iniciar sesión");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-[#3C3563]">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-80">
        <h1 className="text-center text-xl font-semibold mb-4 text-[#3C3563]">
          Joyería Dubái
        </h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Usuario"
            className="border p-2 w-full mb-3 rounded-md"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Contraseña"
            className="border p-2 w-full mb-4 rounded-md"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            className="bg-[#6A4FB8] text-white w-full py-2 rounded-md"
          >
            Iniciar Sesión
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;

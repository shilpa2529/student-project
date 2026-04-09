"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import "../styles/auth.css";

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

 const handleLogin = async () => {
  try {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    router.push("/students"); // redirect after login
    console.log(data);
    } 
  catch (err) {
    console.error("Detailed error:", err);
   }
};
  return (
    <div className="container">
      <h2>Login</h2>
      <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
      <p onClick={() => router.push("/register")}>Create account</p>
    </div>
  );
}
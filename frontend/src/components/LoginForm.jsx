import { useState } from "react";

import api from "../api/client";


function LoginForm({
  setIsAuthenticated,
}) {
  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [message, setMessage] =
    useState("");
    
  async function handleLogin() {

    try {
      const response =
        await api.post(
          "/auth/login",
          {
            username,
            password,
          }
        );

      // Save JWT token
      localStorage.setItem(
        "token",
        response.data.access_token
      );

      setMessage(
        "Login successful."
      );
      setIsAuthenticated(
        true
      );

    } catch (error) {
      console.error(error);
      setMessage(
        "Login failed."
      );
    }
  }

  return (

    <div>
      <h2>Login</h2>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(event) =>
          setUsername(
            event.target.value
          )
        }
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) =>
          setPassword(
            event.target.value
          )
        }
      />

      <button
        type="button"
        onClick={handleLogin}
      >
        Login
      </button>

      {message && (
        <p>{message}</p>
      )}

    </div>
  );
}

export default LoginForm;
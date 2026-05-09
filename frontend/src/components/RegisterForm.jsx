import { useState } from "react";

import api from "../api/client";

function RegisterForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleRegister() {
    try {
      await api.post(
        "/auth/register",

        {
          username,
          password,
        }
      );
      setMessage(
        "Registration successful."
      );

    } catch (error) {
      console.error(error);
      setMessage(
        "Registration failed."
      );
    }
  }


  return (

    <div>

      <h2>Register</h2>

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
        onClick={handleRegister}
      >
        Register
      </button>
      {message && (
        <p>{message}</p>
      )}

    </div>
  );
}

export default RegisterForm;
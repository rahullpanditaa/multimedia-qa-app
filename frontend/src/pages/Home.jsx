import { useState } from "react";

import FileUpload from "../components/FileUpload";
import ChatBox from "../components/ChatBox";
import SummaryPanel from "../components/SummaryPanel";
import TimestampResults from "../components/TimestampResults";

import LoginForm from "../components/LoginForm";
import RegisterForm from "../components/RegisterForm";


function Home() {

  // auth state
  const [isAuthenticated, setIsAuthenticated] =
    useState(!!localStorage.getItem("token"));

  // Toggle between login and register forms
  const [showRegister, setShowRegister] = useState(false);

  // Logout handler func
  function handleLogout() {
    // Remove JWT token
    localStorage.removeItem("token");

    // Return to login screen.
    setIsAuthenticated(false);
  }

  if (!isAuthenticated) {
    return (
      <div className="app-container">
        <div className="section-card">
          {showRegister ? (
            <>
              <RegisterForm />
              <p>
                Already have an account?
              </p>

              <button
                type="button"
                onClick={() => setShowRegister(false)}
              >
                Go to Login
              </button>
            </>

          ) : (
            <>
              <LoginForm
                setIsAuthenticated={
                  setIsAuthenticated
                }
              />

              <p>
                Don't have an account?
              </p>

              <button
                type="button"
                onClick={() => setShowRegister(true)}
              >
                Create Account
              </button>
            </>

          )}

        </div>
      </div>
    );
  }
  
  return (

    <div className="app-container">

      {/* Page title and logout button */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <h1 className="page-title">
          Multimedia RAG Application
        </h1>

        <button
          type="button"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>


      {/* Upload section */}
      <div className="section-card">
        <FileUpload />
      </div>


      {/* Chat section */}
      <div className="section-card">
        <ChatBox />
      </div>


      {/* Summary section */}
      <div className="section-card">
        <SummaryPanel />
      </div>


      {/* Timestamp section */}
      <div className="section-card">
        <TimestampResults />
      </div>

    </div>
  );
}


export default Home;
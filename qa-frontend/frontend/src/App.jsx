import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import InterviewerDashboard from "./components/interviewer/Dashboard";
import IntervieweeDashboard from "./components/interviewee/Dashboard";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Navbar from "./components/common/Navbar";
import "./index.css";

function App() {
  return (
    <AuthProvider>
      <div className="app">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/interviewer/*"
              element={
                <ProtectedRoute role="interviewer">
                  <InterviewerDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/interviewee/*"
              element={
                <ProtectedRoute role="interviewee">
                  <IntervieweeDashboard />
                </ProtectedRoute>
              }
            />
            <Route path="/" element={<div><b>Welcome to the zone</b><br/><i>login or Register to continue</i></div>} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;

import React from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { Navigate } from 'react-router-dom'

const ProtectedRoute = ({ children, role }) => {
  const { currentUser } = useAuth()
  const token = localStorage.getItem('token') // Added this line

  if (!token || !currentUser) {
    return <Navigate to="/login" replace />
  }

  if (role && currentUser.role !== role) {
    return <Navigate to="/" replace />
  }

  return children
}

export default ProtectedRoute
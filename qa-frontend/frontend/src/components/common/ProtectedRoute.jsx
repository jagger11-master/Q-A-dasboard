 
import { Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

const ProtectedRoute = ({ children, role }) => {
  const { user } = useAuth()
  const token = localStorage.getItem('token')

  if (!token || !user) {
    return <Navigate to="/login" replace />
  }

  if (role && user.role.toLowerCase() !== role.toLowerCase()) {
    return <Navigate to="/" replace />
  }

  return children
}

export default ProtectedRoute
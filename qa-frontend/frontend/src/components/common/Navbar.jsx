import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

const Navbar = () => {
  const { currentUser, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          Q&A Zone
        </Link>
        <div className="nav-menu">
          {currentUser ? (
            <>
              <span className="nav-user">Welcome, {currentUser.name}</span>
              <Link 
                to={currentUser.role === 'interviewer' ? '/interviewer' : '/interviewee'} 
                className="nav-link"
              >
                Dashboard
              </Link>
              <button onClick={handleLogout} className="nav-link btn-link">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">
                Login
              </Link>
              <Link to="/register" className="nav-link">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
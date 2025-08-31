import React, { useState, useEffect } from 'react'
import { api } from '../../services/api'
import QuestionnaireForm from './QuestionnaireForm'
import ResponseView from './ResponseView'

const InterviewerDashboard = () => {
  const [questionnaires, setQuestionnaires] = useState([])
  const [selectedQuestionnaire, setSelectedQuestionnaire] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchQuestionnaires()
  }, [])

  const fetchQuestionnaires = async () => {
    try {
      const response = await api.get('/questionnaires')
      setQuestionnaires(response.data)
    } catch (error) {
      console.error('Failed to fetch questionnaires', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateQuestionnaire = () => {
    setShowForm(true)
    setSelectedQuestionnaire(null)
  }

  const handleViewResponses = (questionnaire) => {
    setSelectedQuestionnaire(questionnaire)
    setShowForm(false)
  }

  const handleFormClose = () => {
    setShowForm(false)
    fetchQuestionnaires()
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="dashboard">
      <h1>Interviewer Dashboard</h1>
      
      {showForm ? (
        <QuestionnaireForm 
          onClose={handleFormClose} 
          questionnaire={selectedQuestionnaire} 
        />
      ) : selectedQuestionnaire ? (
        <ResponseView 
          questionnaire={selectedQuestionnaire} 
          onBack={() => setSelectedQuestionnaire(null)} 
        />
      ) : (
        <>
          <button onClick={handleCreateQuestionnaire} className="btn-primary">
            Create New Questionnaire
          </button>
          
          <div className="questionnaire-list">
            <h2>Your Questionnaires</h2>
            {questionnaires.length === 0 ? (
              <p>No questionnaires yet. Create your first one!</p>
            ) : (
              <div className="card-grid">
                {questionnaires.map((q) => (
                  <div key={q.id} className="card">
                    <h3>{q.title}</h3>
                    <p>{q.description}</p>
                    <p>{q.question_count} questions</p>
                    <button 
                      onClick={() => handleViewResponses(q)}
                      className="btn-secondary"
                    >
                      View Responses
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default InterviewerDashboard
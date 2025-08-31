import React, { useState, useEffect } from 'react'
import { api } from '../../services/api'
import QuestionnaireList from './QuestionnaireList'

const IntervieweeDashboard = () => {
  const [questionnaires, setQuestionnaires] = useState([])
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

  if (loading) return <div>Loading questionnaires...</div>

  return (
    <div className="dashboard">
      <h1>Interviewee Dashboard</h1>
      <p>Select a questionnaire to respond to:</p>
      
      <QuestionnaireList questionnaires={questionnaires} />
    </div>
  )
}

export default IntervieweeDashboard
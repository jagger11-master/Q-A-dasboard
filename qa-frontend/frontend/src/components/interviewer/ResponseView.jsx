import React, { useState, useEffect } from 'react'
import { api } from '../../services/api'

const ResponseView = ({ questionnaire, onBack }) => {
  const [responses, setResponses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchResponses()
  }, [questionnaire])

  const fetchResponses = async () => {
    try {
      const response = await api.get(`/questionnaires/${questionnaire.id}/responses`)
      setResponses(response.data)
    } catch (error) {
      console.error('Failed to fetch responses', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading responses...</div>

  return (
    <div className="response-view">
      <button onClick={onBack} className="btn-secondary">
        Back to Questionnaires
      </button>

      <h2>Responses for: {questionnaire.title}</h2>
      
      {responses.length === 0 ? (
        <p>No responses yet.</p>
      ) : (
        responses.map((response) => (
          <div key={response.response_id} className="response-item">
            <div className="response-header">
              <div>
                <strong>{response.interviewee_name}</strong> ({response.interviewee_email})
              </div>
              <div>Submitted on: {new Date(response.submitted_at).toLocaleString()}</div>
            </div>

            <div className="answers-list">
              {response.answers.map((answer, index) => (
                <div key={index} className="answer-item">
                  <strong>Q: {answer.question_text}</strong>
                  <p>A: {answer.answer_text}</p>
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  )
}

export default ResponseView
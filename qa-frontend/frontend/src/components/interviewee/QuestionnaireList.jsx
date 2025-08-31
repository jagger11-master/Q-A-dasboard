import React, { useState } from 'react'
import { api } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

const QuestionnaireList = ({ questionnaires }) => {
  const { currentUser } = useAuth()
  const [selectedQuestionnaire, setSelectedQuestionnaire] = useState(null)
  const [answers, setAnswers] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  const handleSelectQuestionnaire = (questionnaire) => {
    setSelectedQuestionnaire(questionnaire)
    // Initialize answers object with empty strings for each question
    const initialAnswers = {}
    questionnaire.questions.forEach((q) => {
      initialAnswers[q.id] = ''
    })
    setAnswers(initialAnswers)
  }

  const handleAnswerChange = (questionId, value) => {
    setAnswers({
      ...answers,
      [questionId]: value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setMessage('')

    try {
      const formattedAnswers = Object.keys(answers).map((questionId) => ({
        question_id: questionId,
        answer_text: answers[questionId]
      }))

      await api.post('/responses', {
        questionnaire_id: selectedQuestionnaire.id,
        answers: formattedAnswers
      })

      setMessage('Response submitted successfully!')
      setSelectedQuestionnaire(null)
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to submit response')
    } finally {
      setSubmitting(false)
    }
  }

  if (selectedQuestionnaire) {
    return (
      <div className="questionnaire-response">
        <button onClick={() => setSelectedQuestionnaire(null)} className="btn-secondary">
          Back to List
        </button>

        <h2>{selectedQuestionnaire.title}</h2>
        <p>{selectedQuestionnaire.description}</p>

        <form onSubmit={handleSubmit}>
          {selectedQuestionnaire.questions.map((question, index) => (
            <div key={question.id} className="form-group">
              <label>
                {index + 1}. {question.question_text}
              </label>
              
              {question.question_type === 'text' && (
                <input
                  type="text"
                  value={answers[question.id] || ''}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  required
                />
              )}

              {question.question_type === 'multiple_choice' && (
                <select
                  value={answers[question.id] || ''}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  required
                >
                  <option value="">Select an option</option>
                  {question.options.map((option, idx) => (
                    <option key={idx} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              )}
            </div>
          ))}

          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? 'Submitting...' : 'Submit Responses'}
          </button>
        </form>

        {message && (
          <div className={message.includes('Failed') ? 'error-message' : 'success-message'}>
            {message}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="questionnaire-list">
      {questionnaires.length === 0 ? (
        <p>No questionnaires available at the moment.</p>
      ) : (
        <div className="card-grid">
          {questionnaires.map((questionnaire) => (
            <div key={questionnaire.id} className="questionnaire-card" onClick={() => handleSelectQuestionnaire(questionnaire)}>
              <h3>{questionnaire.title}</h3>
              <p>{questionnaire.description}</p>
              <div className="questionnaire-meta">
                {questionnaire.question_count} questions
              </div>
              <button className="btn-primary">Respond</button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default QuestionnaireList
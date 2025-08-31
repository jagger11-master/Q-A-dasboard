import React, { useState } from 'react'
import { api } from '../../services/api'

const QuestionnaireForm = ({ onClose, questionnaire }) => {
  const [title, setTitle] = useState(questionnaire ? questionnaire.title : '')
  const [description, setDescription] = useState(questionnaire ? questionnaire.description : '')
  const [questions, setQuestions] = useState(questionnaire ? questionnaire.questions : [])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const addQuestion = () => {
    setQuestions([...questions, { question_text: '', question_type: 'text', options: null }])
  }

  const removeQuestion = (index) => {
    const newQuestions = [...questions]
    newQuestions.splice(index, 1)
    setQuestions(newQuestions)
  }

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...questions]
    newQuestions[index][field] = value
    setQuestions(newQuestions)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const payload = { title, description, questions }
      if (questionnaire) {
        await api.put(`/questionnaires/${questionnaire.id}`, payload)
      } else {
        await api.post('/questionnaires', payload)
      }
      onClose()
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to save questionnaire')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="questionnaire-form">
      <h2>{questionnaire ? 'Edit' : 'Create'} Questionnaire</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="3"
          />
        </div>

        <div className="questions-section">
          <h3>Questions</h3>
          {questions.map((question, index) => (
            <div key={index} className="question-item">
              <div className="form-group">
                <label>Question {index + 1}</label>
                <input
                  type="text"
                  value={question.question_text}
                  onChange={(e) => updateQuestion(index, 'question_text', e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Type</label>
                <select
                  value={question.question_type}
                  onChange={(e) => updateQuestion(index, 'question_type', e.target.value)}
                >
                  <option value="text">Text</option>
                  <option value="multiple_choice">Multiple Choice</option>
                </select>
              </div>

              {question.question_type === 'multiple_choice' && (
                <div className="form-group">
                  <label>Options (comma separated)</label>
                  <input
                    type="text"
                    value={question.options ? question.options.join(',') : ''}
                    onChange={(e) => updateQuestion(index, 'options', e.target.value.split(','))}
                  />
                </div>
              )}

              <button
                type="button"
                onClick={() => removeQuestion(index)}
                className="btn-secondary"
              >
                Remove Question
              </button>
            </div>
          ))}

          <button type="button" onClick={addQuestion} className="btn-secondary">
            Add Question
          </button>
        </div>

        <div className="form-actions">
          <button type="button" onClick={onClose} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Saving...' : 'Save Questionnaire'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default QuestionnaireForm
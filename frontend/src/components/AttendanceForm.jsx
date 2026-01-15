import { useState } from 'react'
import axios from 'axios'
import './AttendanceForm.css'

const AttendanceForm = () => {
  const [formData, setFormData] = useState({
    student_name: '',
    register_number: '',
    date: new Date().toISOString().split('T')[0],
    status: 'Present',
    reason: ''
  })

  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)
  const [messageType, setMessageType] = useState(null) // 'success', 'clarification', 'error'

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Clear reason when status changes to Present
    if (name === 'status' && value === 'Present') {
      setFormData(prev => ({
        ...prev,
        reason: ''
      }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)
    setMessageType(null)

    try {
      const response = await axios.post('/api/attendance', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.data.clarification_question) {
        setMessageType('clarification')
        setMessage(response.data.clarification_question)
      } else if (response.data.confirmation_message) {
        setMessageType('success')
        setMessage(response.data.confirmation_message)
        // Reset form after successful submission
        setFormData({
          student_name: '',
          register_number: '',
          date: new Date().toISOString().split('T')[0],
          status: 'Present',
          reason: ''
        })
      }
    } catch (error) {
      setMessageType('error')
      setMessage(
        error.response?.data?.detail || 
        error.message || 
        'An error occurred while submitting attendance'
      )
    } finally {
      setLoading(false)
    }
  }

  const requiresReason = formData.status === 'Absent'

  return (
    <div className="attendance-form-container">
      <form onSubmit={handleSubmit} className="attendance-form">
        <div className="form-group">
          <label htmlFor="student_name">
            Student Name <span className="required">*</span>
          </label>
          <input
            type="text"
            id="student_name"
            name="student_name"
            value={formData.student_name}
            onChange={handleChange}
            required
            placeholder="Enter student full name"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="register_number">
            Register Number <span className="required">*</span>
          </label>
          <input
            type="text"
            id="register_number"
            name="register_number"
            value={formData.register_number}
            onChange={handleChange}
            required
            placeholder="Enter register number"
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="date">
            Date <span className="required">*</span>
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="status">
            Attendance Status <span className="required">*</span>
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            required
            className="form-select"
          >
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
        </div>

        {requiresReason && (
          <div className="form-group">
            <label htmlFor="reason">
              Reason <span className="required">*</span>
            </label>
            <input
              type="text"
              id="reason"
              name="reason"
              value={formData.reason}
              onChange={handleChange}
              required={requiresReason}
              placeholder={`Enter reason for ${formData.status.toLowerCase()}`}
              className="form-input"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="submit-button"
        >
          {loading ? 'Submitting...' : 'Submit Attendance'}
        </button>
      </form>

      {message && (
        <div className={`message ${messageType}`}>
          <div className="message-content">
            {messageType === 'success' && <span className="message-icon">✓</span>}
            {messageType === 'clarification' && <span className="message-icon">?</span>}
            {messageType === 'error' && <span className="message-icon">✗</span>}
            <p>{message}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default AttendanceForm

import { useState } from 'react'
import axios from 'axios'
import './AttendanceForm.css'
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY

const AttendanceForm = () => {
  const [formData, setFormData] = useState({
    student_name: '',
    register_number: '',
    date: new Date().toISOString().split('T')[0],
    status: 'Present',
    reason: ''
  })

  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

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
    setSuccessMessage('')

    try {
      await axios.post(
        `${import.meta.env.VITE_SUPABASE_URL}/rest/v1/attendance`,
        formData,
        {
          headers: {
            'Content-Type': 'application/json',
            apikey: import.meta.env.VITE_SUPABASE_ANON_KEY,
            Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
            Prefer: 'return=representation'
          }
        }
      )
      // Show success message
      setSuccessMessage('your attendance has mark')
    } catch (error) {
      // Silently handle errors - don't show anything
    } finally {
      setLoading(false)
      // Always reset form after submission
      setFormData({
        student_name: '',
        register_number: '',
        date: new Date().toISOString().split('T')[0],
        status: 'Present',
        reason: ''
      })
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

      {successMessage && (
        <div className="message success">
          <div className="message-content">
            <span className="message-icon">✓</span>
            <p>{successMessage}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default AttendanceForm

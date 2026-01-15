import { useState } from 'react'
import AttendanceForm from './components/AttendanceForm'
import './App.css'

function App() {
  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <h1>Smart Attendance Assistant</h1>
          <p className="subtitle">College Faculty Attendance Management System</p>
        </header>
        <main className="app-main">
          <AttendanceForm />
        </main>
      </div>
    </div>
  )
}

export default App

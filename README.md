# Smart Attendance Assistant

A form-based attendance management system for college faculty with AI-powered validation and structured data storage.

## Features

- **Form-based UI**: Clean, professional attendance form (no chat interface)
- **AI Validation**: LangGraph workflow validates and processes attendance records
- **Multiple Status Types**: Present, Late, Absent, Leave
- **Smart Clarifications**: AI asks for missing information when needed
- **Database Storage**: Supabase PostgreSQL for persistent storage
- **Confirmation Messages**: AI-generated confirmations after successful submissions

## Tech Stack

### Frontend
- React 18
- Vite
- Axios

### Backend
- Python 3.9+
- FastAPI
- LangGraph
- LangChain
- OpenAI API

### Database
- Supabase (PostgreSQL)

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- OpenAI API key

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Supabase Setup

1. Create a new Supabase project
2. Run the SQL schema from `backend/supabase_schema.sql` in the Supabase SQL editor
3. Copy your project URL and anon key to the `.env` file

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Running the Application

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

**Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### POST /attendance

Submit attendance record.

**Request Body:**
```json
{
  "student_name": "John Doe",
  "register_number": "REG123",
  "date": "2026-01-15",
  "status": "Late",
  "reason": "Traffic delay"
}
```

**Response:**
```json
{
  "confirmation_message": "Attendance recorded: John Doe (Register No: REG123) marked as Late on 2026-01-15. Reason: Traffic delay.",
  "clarification_question": null,
  "attendance_status": "Late"
}
```

If clarification is needed:
```json
{
  "confirmation_message": null,
  "clarification_question": "Please provide a reason for the Late status.",
  "attendance_status": null
}
```

## LangGraph Workflow

The system uses a LangGraph workflow with the following nodes:

1. **Start Node**: Receives form submission data
2. **Router Node**: Validates status and routes to appropriate node
3. **Attendance Nodes**: 
   - Present Node
   - Late Node
   - Absent Node
   - Leave Node

Each node validates required fields and stores the record in Supabase when complete.

## Project Structure

```
.
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AttendanceForm.jsx
│   │   │   └── AttendanceForm.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── langgraph_workflow.py
│   ├── supabase_client.py
│   ├── requirements.txt
│   ├── .env.example
│   └── supabase_schema.sql
└── README.md
```

## Notes

- The system asks for clarification only when required data is missing
- Reason field is required only for "Late" and "Leave" statuses
- All attendance records are stored in Supabase with timestamps
- The UI is designed to look professional and academic, not experimental

## License

MIT

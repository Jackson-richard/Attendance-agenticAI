# Quick Setup Guide

## Step 1: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file (copy from `env.example`):
```bash
# Copy env.example to .env and fill in your credentials
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

## Step 2: Supabase Setup

1. Go to [Supabase](https://supabase.com) and create a new project
2. Open the SQL Editor in your Supabase dashboard
3. Run the SQL from `backend/supabase_schema.sql` to create the attendance table
4. Go to Settings > API to get your:
   - Project URL (SUPABASE_URL)
   - Anon/Public Key (SUPABASE_KEY)

## Step 3: Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Step 4: Run the Application

### Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload
```
Backend runs on: http://localhost:8000

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:3000

## Testing

1. Open http://localhost:3000 in your browser
2. Fill out the attendance form
3. Submit and check for confirmation message
4. Verify the record in your Supabase dashboard

## Troubleshooting

- **Backend errors**: Check that `.env` file has correct credentials
- **CORS errors**: Ensure backend is running on port 8000
- **Database errors**: Verify Supabase table was created correctly
- **Frontend not loading**: Check that `npm install` completed successfully

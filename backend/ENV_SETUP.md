# Environment Variables Setup

## Creating your .env file

1. Copy the example file:
   ```powershell
   cd backend
   copy .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:

### Format for SUPABASE_URL:
```
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
```

**Important:**
- ✅ **DO include** `https://` at the beginning
- ✅ **DO NOT include** `/rest/v1` at the end (the code adds this automatically)
- ✅ **DO NOT include** trailing slashes

### Format for SUPABASE_KEY:
```
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNjIzOTAyMCwiZXhwIjoxOTMxODE1MDIwfQ.example
```

### Where to find these values:

1. Go to your Supabase project dashboard
2. Click on **Settings** (gear icon)
3. Click on **API**
4. Find:
   - **Project URL** → Copy this as `SUPABASE_URL`
   - **anon public** key → Copy this as `SUPABASE_KEY`

### Example .env file:
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Troubleshooting

If you get "Request URL is missing an 'http://' or 'https://' protocol":
- Make sure your `SUPABASE_URL` starts with `https://`
- The code will auto-add `https://` if missing, but it's better to include it

If you get connection errors:
- Verify your Supabase project is active
- Check that the URL and key are correct (no extra spaces)
- Make sure you're using the **anon/public** key, not the service_role key

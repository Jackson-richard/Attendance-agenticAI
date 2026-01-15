from postgrest import SyncPostgrestClient
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def get_supabase_client():
    """Get Supabase PostgREST client instance"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
            "Please create a .env file in the backend directory with these values."
        )
    
    # Clean and validate URL
    supabase_url = supabase_url.strip()
    supabase_key = supabase_key.strip()
    
    # Remove any quotes that might have been added
    supabase_url = supabase_url.strip('"').strip("'")
    supabase_key = supabase_key.strip('"').strip("'")
    
    # Check if still using placeholder values (only check for obvious placeholders)
    placeholder_urls = ["your_supabase_project_url", "your-project-id.supabase.co"]
    placeholder_keys = ["your_supabase_anon_key", "your_anon_key"]
    
    if supabase_url.lower() in [p.lower() for p in placeholder_urls]:
        raise ValueError(
            "Please update SUPABASE_URL in your .env file with your actual Supabase project URL. "
            "Format: SUPABASE_URL=https://your-project-id.supabase.co"
        )
    
    if supabase_key.lower() in [p.lower() for p in placeholder_keys]:
        raise ValueError(
            "Please update SUPABASE_KEY in your .env file with your actual Supabase anon key. "
            "Get it from: Supabase Dashboard > Settings > API > anon public key"
        )
    
    # Ensure URL has protocol
    if not supabase_url.startswith(("http://", "https://")):
        supabase_url = f"https://{supabase_url}"
    
    # Remove trailing slash if present
    supabase_url = supabase_url.rstrip("/")
    
    # Construct the PostgREST API URL
    base_url = f"{supabase_url}/rest/v1"
    
    try:
        return SyncPostgrestClient(
            base_url=base_url,
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        raise Exception(
            f"Failed to create Supabase client. URL: {base_url}. "
            f"Error: {str(e)}. Please check your SUPABASE_URL and SUPABASE_KEY in .env file."
        )


def store_attendance(
    student_name: str,
    register_number: str,
    date: str,
    status: str,
    reason: Optional[str] = None
) -> dict:
    """Store attendance record in Supabase"""
    client = get_supabase_client()
    
    data = {
        "student_name": student_name,
        "register_number": register_number,
        "date": date,
        "status": status,
        "reason": reason
    }
    
    result = client.from_("attendance").insert(data).execute()
    
    if not result.data:
        raise Exception("Failed to store attendance record")
    
    return result.data[0]

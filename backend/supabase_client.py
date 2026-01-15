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
    
    return SyncPostgrestClient(
        base_url=f"{supabase_url}/rest/v1",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from langgraph_workflow import process_attendance
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Smart Attendance Assistant API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AttendanceRequest(BaseModel):
    student_name: str
    register_number: str
    date: str
    status: str
    reason: Optional[str] = None


class AttendanceResponse(BaseModel):
    confirmation_message: Optional[str] = None
    clarification_question: Optional[str] = None
    attendance_status: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Smart Attendance Assistant API"}


@app.post("/attendance", response_model=AttendanceResponse)
async def submit_attendance(request: AttendanceRequest):
    try:
        result = await process_attendance(
            student_name=request.student_name,
            register_number=request.register_number,
            date=request.date,
            status=request.status,
            reason=request.reason
        )
        
        return AttendanceResponse(
            confirmation_message=result.get("confirmation_message"),
            clarification_question=result.get("clarification_question"),
            attendance_status=result.get("attendance_status")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

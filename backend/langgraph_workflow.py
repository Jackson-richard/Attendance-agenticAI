from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from supabase_client import store_attendance


class AttendanceState(TypedDict):
    student_name: str
    register_number: str
    date: str
    status: str
    reason: Optional[str]
    clarification_question: Optional[str]
    confirmation_message: Optional[str]
    attendance_status: Optional[str]
    is_complete: bool


def start_node(state: AttendanceState) -> AttendanceState:
    """Initial node that receives form data"""
    return state


def router_node(state: AttendanceState) -> AttendanceState:
    """Routes to appropriate attendance node based on status"""
    status = state.get("status", "").lower()
    
    # Validate status
    valid_statuses = ["present", "absent"]
    if status not in valid_statuses:
        return {
            **state,
            "clarification_question": f"Invalid attendance status. Please select one of: Present or Absent.",
            "is_complete": False
        }
    
    return state


def validate_required_fields(state: AttendanceState, required_reason: bool = False) -> tuple[bool, Optional[str]]:
    """Validates all required fields are present"""
    student_name = state.get("student_name", "").strip()
    register_number = state.get("register_number", "").strip()
    date = state.get("date", "").strip()
    reason = state.get("reason", "").strip() if required_reason else ""
    
    if not student_name:
        return False, "Please provide the student's full name."
    
    if not register_number:
        return False, "Please provide the student's register number."
    
    if not date:
        return False, "Please provide the attendance date."
    
    if required_reason and not reason:
        return False, f"Please provide a reason for the {state.get('status', '')} status."
    
    return True, None


def present_node(state: AttendanceState) -> AttendanceState:
    """Handles Present attendance status"""
    is_valid, error_msg = validate_required_fields(state, required_reason=False)
    
    if not is_valid:
        return {
            **state,
            "clarification_question": error_msg,
            "is_complete": False
        }
    
    # Store attendance
    try:
        store_attendance(
            student_name=state["student_name"],
            register_number=state["register_number"],
            date=state["date"],
            status="Present",
            reason=None
        )
        
        confirmation = (
            f"Attendance recorded: {state['student_name']} (Register No: {state['register_number']}) "
            f"marked as Present on {state['date']}."
        )
        
        return {
            **state,
            "confirmation_message": confirmation,
            "attendance_status": "Present",
            "is_complete": True
        }
    except Exception as e:
        return {
            **state,
            "clarification_question": f"Error storing attendance: {str(e)}",
            "is_complete": False
        }


def late_node(state: AttendanceState) -> AttendanceState:
    """Handles Late attendance status"""
    is_valid, error_msg = validate_required_fields(state, required_reason=True)
    
    if not is_valid:
        return {
            **state,
            "clarification_question": error_msg,
            "is_complete": False
        }
    
    # Store attendance
    try:
        store_attendance(
            student_name=state["student_name"],
            register_number=state["register_number"],
            date=state["date"],
            status="Late",
            reason=state.get("reason")
        )
        
        confirmation = (
            f"Attendance recorded: {state['student_name']} (Register No: {state['register_number']}) "
            f"marked as Late on {state['date']}. Reason: {state.get('reason', 'N/A')}."
        )
        
        return {
            **state,
            "confirmation_message": confirmation,
            "attendance_status": "Late",
            "is_complete": True
        }
    except Exception as e:
        return {
            **state,
            "clarification_question": f"Error storing attendance: {str(e)}",
            "is_complete": False
        }


def absent_node(state: AttendanceState) -> AttendanceState:
    """Handles Absent attendance status"""
    is_valid, error_msg = validate_required_fields(state, required_reason=True)
    
    if not is_valid:
        return {
            **state,
            "clarification_question": error_msg,
            "is_complete": False
        }
    
    # Store attendance
    try:
        store_attendance(
            student_name=state["student_name"],
            register_number=state["register_number"],
            date=state["date"],
            status="Absent",
            reason=state.get("reason")
        )
        
        confirmation = (
            f"Attendance recorded: {state['student_name']} (Register No: {state['register_number']}) "
            f"marked as Absent on {state['date']}. Reason: {state.get('reason', 'N/A')}."
        )
        
        return {
            **state,
            "confirmation_message": confirmation,
            "attendance_status": "Absent",
            "is_complete": True
        }
    except Exception as e:
        return {
            **state,
            "clarification_question": f"Error storing attendance: {str(e)}",
            "is_complete": False
        }


def route_after_router(state: AttendanceState) -> str:
    """Routes to appropriate attendance node after validation"""
    status = state.get("status", "").lower()
    
    if "clarification_question" in state and state["clarification_question"]:
        return END
    
    status_map = {
        "present": "present_node",
        "absent": "absent_node"
    }
    
    return status_map.get(status, END)


# Build the graph
workflow = StateGraph(AttendanceState)

# Add nodes
workflow.add_node("start_node", start_node)
workflow.add_node("router_node", router_node)
workflow.add_node("present_node", present_node)
workflow.add_node("absent_node", absent_node)

# Add edges
workflow.set_entry_point("start_node")
workflow.add_edge("start_node", "router_node")
workflow.add_conditional_edges(
    "router_node",
    route_after_router,
    {
        "present_node": "present_node",
        "absent_node": "absent_node",
        END: END
    }
)
workflow.add_edge("present_node", END)
workflow.add_edge("absent_node", END)

# Compile the graph
app = workflow.compile()


async def process_attendance(
    student_name: str,
    register_number: str,
    date: str,
    status: str,
    reason: Optional[str] = None
) -> dict:
    """Process attendance through LangGraph workflow"""
    initial_state = {
        "student_name": student_name,
        "register_number": register_number,
        "date": date,
        "status": status,
        "reason": reason,
        "clarification_question": None,
        "confirmation_message": None,
        "attendance_status": None,
        "is_complete": False
    }
    
    # Run the workflow
    result = await app.ainvoke(initial_state)
    
    return {
        "confirmation_message": result.get("confirmation_message"),
        "clarification_question": result.get("clarification_question"),
        "attendance_status": result.get("attendance_status")
    }

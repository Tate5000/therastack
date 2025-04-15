"""
Consolidated Clinical Operations Service
- Calendar and appointments
- Messaging
- Call management
- AI Assistance
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class Appointment(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    therapist_id: str
    therapist_name: str
    start_time: str
    end_time: str
    status: str  # scheduled, confirmed, cancelled, completed
    type: str  # initial, follow-up, group, etc.
    notes: Optional[str] = None
    created_at: str
    updated_at: str

class AppointmentCreate(BaseModel):
    patient_id: str
    patient_name: str
    therapist_id: str
    therapist_name: str
    start_time: str
    end_time: str
    type: str
    notes: Optional[str] = None

class Message(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    sender_name: str
    receiver_id: str
    receiver_name: str
    content: str
    sent_at: str
    read_at: Optional[str] = None

class MessageCreate(BaseModel):
    conversation_id: str
    sender_id: str
    sender_name: str
    receiver_id: str
    receiver_name: str
    content: str

class CallSession(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    therapist_id: str
    therapist_name: str
    start_time: str
    end_time: Optional[str] = None
    status: str  # scheduled, in-progress, completed, cancelled
    recording_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str

class AIAssistant(BaseModel):
    id: str
    user_id: str
    query: str
    response: str
    created_at: str

# Mock databases
appointments_db = {}
messages_db = {}
conversations_db = {}
call_sessions_db = {}
ai_queries_db = {}

# Router
router = APIRouter(
    prefix="/api/clinical",
    tags=["clinical"],
    responses={404: {"description": "Not found"}},
)

# Routes - Appointments
@router.get("/appointments", response_model=List[Appointment])
async def get_appointments(
    patient_id: Optional[str] = None,
    therapist_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get appointments with optional filters"""
    appointments = list(appointments_db.values())
    
    if patient_id:
        appointments = [appt for appt in appointments if appt.patient_id == patient_id]
    
    if therapist_id:
        appointments = [appt for appt in appointments if appt.therapist_id == therapist_id]
    
    if status:
        appointments = [appt for appt in appointments if appt.status == status]
    
    if start_date:
        appointments = [appt for appt in appointments if appt.start_time >= start_date]
    
    if end_date:
        appointments = [appt for appt in appointments if appt.start_time <= end_date]
    
    return appointments

@router.post("/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate):
    """Create a new appointment"""
    new_appointment = Appointment(
        id=str(uuid.uuid4()),
        **appointment.dict(),
        status="scheduled",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    appointments_db[new_appointment.id] = new_appointment
    
    return new_appointment

# Routes - Messages
@router.get("/messages/{conversation_id}", response_model=List[Message])
async def get_conversation_messages(conversation_id: str):
    """Get all messages in a conversation"""
    messages = [msg for msg in messages_db.values() if msg.conversation_id == conversation_id]
    
    # Sort by sent_at
    messages.sort(key=lambda x: x.sent_at)
    
    return messages

@router.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageCreate):
    """Create a new message"""
    new_message = Message(
        id=str(uuid.uuid4()),
        **message.dict(),
        sent_at=datetime.now().isoformat(),
        read_at=None
    )
    
    messages_db[new_message.id] = new_message
    
    return new_message

# Routes - Call Sessions
@router.get("/calls", response_model=List[CallSession])
async def get_call_sessions(
    patient_id: Optional[str] = None,
    therapist_id: Optional[str] = None,
    status: Optional[str] = None
):
    """Get call sessions with optional filters"""
    calls = list(call_sessions_db.values())
    
    if patient_id:
        calls = [call for call in calls if call.patient_id == patient_id]
    
    if therapist_id:
        calls = [call for call in calls if call.therapist_id == therapist_id]
    
    if status:
        calls = [call for call in calls if call.status == status]
    
    return calls

@router.post("/calls", response_model=CallSession, status_code=status.HTTP_201_CREATED)
async def create_call_session(
    patient_id: str,
    patient_name: str,
    therapist_id: str,
    therapist_name: str
):
    """Create a new call session"""
    new_call = CallSession(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        patient_name=patient_name,
        therapist_id=therapist_id,
        therapist_name=therapist_name,
        start_time=datetime.now().isoformat(),
        status="in-progress",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    call_sessions_db[new_call.id] = new_call
    
    return new_call

# Routes - AI Assistant
@router.post("/ai-assistant", response_model=AIAssistant)
async def query_ai_assistant(user_id: str, query: str):
    """Query the AI assistant"""
    # In a real app, this would call an AI model
    response = f"This is a simulated AI response to: {query}"
    
    ai_query = AIAssistant(
        id=str(uuid.uuid4()),
        user_id=user_id,
        query=query,
        response=response,
        created_at=datetime.now().isoformat()
    )
    
    ai_queries_db[ai_query.id] = ai_query
    
    return ai_query

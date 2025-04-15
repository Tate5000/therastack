"""
Consolidated Patient Records Service
- Patient information
- Documents/files (combines patient_docs_s3 and company_docs_s3)
- Visit history
- Notes and transcriptions
"""

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, status
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class Patient(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    created_at: str
    updated_at: str

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None

class Document(BaseModel):
    id: str
    patient_id: str
    name: str
    type: str  # medical_record, insurance, transcription, etc.
    file_path: str
    size: int
    uploaded_by: str
    created_at: str
    updated_at: str

class Visit(BaseModel):
    id: str
    patient_id: str
    therapist_id: str
    date: str
    duration: int  # minutes
    notes: Optional[str] = None
    status: str  # scheduled, completed, cancelled
    created_at: str
    updated_at: str

# Mock databases
patients_db = {}
documents_db = {}
visits_db = {}

# Router
router = APIRouter(
    prefix="/api/patients",
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)

# Routes - Patients
@router.get("/", response_model=List[Patient])
async def get_patients():
    """Get all patients"""
    return list(patients_db.values())

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get a specific patient by ID"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return patients_db[patient_id]

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    """Create a new patient"""
    new_patient = Patient(
        id=str(uuid.uuid4()),
        **patient.dict(),
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    patients_db[new_patient.id] = new_patient
    
    return new_patient

# Routes - Documents
@router.get("/{patient_id}/documents", response_model=List[Document])
async def get_patient_documents(patient_id: str):
    """Get all documents for a patient"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    documents = [doc for doc in documents_db.values() if doc.patient_id == patient_id]
    return documents

@router.post("/{patient_id}/documents")
async def upload_document(
    patient_id: str,
    file: UploadFile,
    document_type: str,
    uploaded_by: str
):
    """Upload a document for a patient"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    # In a real app, we would save the file to S3
    # Here we'll just create the document record
    document = Document(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        name=file.filename,
        type=document_type,
        file_path=f"s3://patient-docs/{patient_id}/{file.filename}",
        size=0,  # Would get actual file size
        uploaded_by=uploaded_by,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    documents_db[document.id] = document
    
    return {"id": document.id, "name": document.name, "type": document.type}

# Routes - Visits
@router.get("/{patient_id}/visits", response_model=List[Visit])
async def get_patient_visits(patient_id: str):
    """Get all visits for a patient"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    visits = [visit for visit in visits_db.values() if visit.patient_id == patient_id]
    return visits

@router.post("/{patient_id}/visits", response_model=Visit, status_code=status.HTTP_201_CREATED)
async def create_visit(
    patient_id: str,
    therapist_id: str,
    date: str,
    duration: int,
    notes: Optional[str] = None
):
    """Create a new visit for a patient"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    visit = Visit(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        therapist_id=therapist_id,
        date=date,
        duration=duration,
        notes=notes,
        status="scheduled",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    visits_db[visit.id] = visit
    
    return visit

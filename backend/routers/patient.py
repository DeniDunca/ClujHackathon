from datetime import datetime
from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Patient, User
from pydantic import BaseModel
from routers.auth import get_current_active_user
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

user_dependency = Annotated[User, Depends(get_current_active_user)]

# Pydantic models for request/response
class PatientBase(BaseModel):
    date_of_birth: datetime
    gender: str
    phone_number: str
    address: str
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    emergency_contact: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
@router.patch("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """Update a patient's profile. Only the patient themselves can update their profile."""
    if user.id != patient_id or user.role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own patient profile"
        )
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Update only provided fields
        update_data = patient_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        patient.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(patient)
        return patient
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating patient: {str(e)}"
        )

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """Get a patient's profile. Only the patient themselves or their doctors can view the profile."""
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Check if user is the patient or a doctor
        if user.id != patient_id and user.role != "doctor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this patient's profile"
            )
        
        return patient
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving patient: {str(e)}"
        )


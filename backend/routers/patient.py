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


# CRUD Operations
@router.post("/create-profile", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_profile(
    patient_data: PatientCreate,
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """
    Create a patient profile for the currently logged-in user.
    This endpoint requires authentication and will link the patient profile to the user's account.
    """
    try:
        # Check if user is already a patient
        existing_patient = db.query(Patient).filter(Patient.id == user.id).first()
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a patient profile"
            )
        
        # Check if user has a different role
        if user.role and user.role.lower() != "patient":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot create patient profile for user with role: {user.role}"
            )
        
        # Update user role to patient
        user.role = "patient"
        user.updated_at = datetime.utcnow()
        
        # Create new patient profile
        db_patient = Patient(
            id=user.id,  # Use the same ID as the user for the relationship
            date_of_birth=patient_data.date_of_birth,
            gender=patient_data.gender,
            phone_number=patient_data.phone_number,
            address=patient_data.address,
            medical_history=patient_data.medical_history,
            allergies=patient_data.allergies,
            current_medications=patient_data.current_medications,
            emergency_contact=patient_data.emergency_contact,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add patient to session
        db.add(db_patient)
        
        # Commit the transaction
        db.commit()
        
        # Refresh the patient object to get all fields
        db.refresh(db_patient)
        
        return db_patient
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating patient profile: {str(e)}"
        )


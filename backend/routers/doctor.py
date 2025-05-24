from datetime import datetime
from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Doctor, User, Patient
from pydantic import BaseModel
from routers.auth import get_current_active_user
from passlib.context import CryptContext
import json

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)

user_dependency = Annotated[User, Depends(get_current_active_user)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models for request/response
class DoctorBase(BaseModel):
    specialization: str
    license_number: str
    years_of_experience: int
    hospital_affiliation: str
    phone_number: str
    address: str
    consultation_fee: float
    available_hours: str  # JSON string
    calendar_id: str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    years_of_experience: Optional[int] = None
    hospital_affiliation: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    consultation_fee: Optional[float] = None
    available_hours: Optional[str] = None
    calendar_id: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/mock-doctor")
async def create_mock_doctor(
    db: Session = Depends(get_db)
):
    """Create a mock doctor for testing purposes."""
    try:
        # Check if mock doctor already exists
        existing_doctor = db.query(Doctor).filter(Doctor.email == "doctor@example.com").first()
        if existing_doctor:
            return {"message": "Mock doctor already exists", "doctor_id": existing_doctor.id}

        # Create mock doctor user
        mock_doctor = Doctor(
            first_name="John",
            last_name="Doe",
            email="doctor@example.com",
            password=pwd_context.hash("doctor123"),
            role="doctor",
            specialization="General Medicine",
            license_number="MD123456",
            years_of_experience=10,
            hospital_affiliation="City Hospital",
            phone_number="+1234567890",
            address="123 Medical Center Dr",
            consultation_fee=100.00,
            available_hours=json.dumps({
                "monday": {"start": "09:00", "end": "17:00"},
                "tuesday": {"start": "09:00", "end": "17:00"},
                "wednesday": {"start": "09:00", "end": "17:00"},
                "thursday": {"start": "09:00", "end": "17:00"},
                "friday": {"start": "09:00", "end": "17:00"}
            }),
            calendar_id="primary"  # Using primary calendar for testing
        )

        db.add(mock_doctor)
        db.commit()
        db.refresh(mock_doctor)

        return {
            "message": "Mock doctor created successfully",
            "doctor_id": mock_doctor.id,
            "email": mock_doctor.email,
            "password": "doctor123"  # Only for testing purposes
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating mock doctor: {str(e)}"
        )

@router.patch("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: int,
    doctor_update: DoctorUpdate,
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """Update a doctor's profile. Only the doctor themselves can update their profile."""
    if user.id != doctor_id or user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own doctor profile"
        )
    
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        # Update only provided fields
        update_data = doctor_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(doctor, field, value)
        
        doctor.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(doctor)
        return doctor
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating doctor: {str(e)}"
        )

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: int,
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """Get a doctor's profile. Any authenticated user can view doctor profiles."""
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        return doctor
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving doctor: {str(e)}"
        )

@router.get("/", response_model=List[DoctorResponse])
async def list_doctors(
    user: user_dependency,
    db: Session = Depends(get_db)
):
    """List all doctors. Any authenticated user can view the list of doctors."""
    try:
        doctors = db.query(Doctor).all()
        return doctors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving doctors: {str(e)}"
        ) 
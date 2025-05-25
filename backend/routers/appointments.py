from datetime import datetime, timedelta
from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, Patient, Doctor, User
from pydantic import BaseModel
from routers.auth import get_current_active_user
import os
import json
from dotenv import load_dotenv

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

# Load environment variables
load_dotenv()

class AppointmentCreate(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    google_event_id: Optional[str]

    class Config:
        orm_mode = True

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Create a new appointment. Only patients can create appointments."""
    if current_user.role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can create appointments"
        )

    try:
        # Verify doctor exists
        doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        # Create appointment in database
        db_appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=appointment.doctor_id,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            notes=appointment.notes,
            status="scheduled"
        )
        db.add(db_appointment)
        db.flush()  # Get the appointment ID

        # Try to create Google Calendar event if credentials exist
        try:
            if os.path.exists('credentials.json') and doctor.calendar_id:
                from google.oauth2.credentials import Credentials
                from google_auth_oauthlib.flow import InstalledAppFlow
                from google.auth.transport.requests import Request
                from googleapiclient.discovery import build

                SCOPES = ['https://www.googleapis.com/auth/calendar']
                TOKEN_FILE = 'token.json'

                creds = None
                if os.path.exists(TOKEN_FILE):
                    with open(TOKEN_FILE, 'r') as token:
                        creds = Credentials.from_authorized_user_info(json.load(token))

                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                    
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())

                service = build('calendar', 'v3', credentials=creds)

                event = {
                    'summary': f'Appointment: {current_user.first_name} {current_user.last_name} with Dr. {doctor.first_name} {doctor.last_name}',
                    'description': appointment.notes or 'Medical appointment',
                    'start': {
                        'dateTime': appointment.start_time.isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': appointment.end_time.isoformat(),
                        'timeZone': 'UTC',
                    },
                }

                event = service.events().insert(
                    calendarId=doctor.calendar_id,
                    body=event
                ).execute()
                
                db_appointment.google_event_id = event['id']
        except Exception as e:
            # Log the error but don't fail the appointment creation
            print(f"Failed to create Google Calendar event: {str(e)}")

        db.commit()
        db.refresh(db_appointment)

        return db_appointment

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating appointment: {str(e)}"
        )

@router.get("/my-appointments", response_model=List[AppointmentResponse])
async def get_appointments(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Get all appointments for the current user."""
    try:
        if current_user.role == "patient":
            appointments = db.query(Appointment).filter(
                Appointment.patient_id == current_user.id
            ).all()
        elif current_user.role == "doctor":
            appointments = db.query(Appointment).filter(
                Appointment.doctor_id == current_user.id
            ).all()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role"
            )
        
        return appointments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving appointments: {str(e)}"
        ) 
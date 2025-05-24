from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from database import Base

# Association table for doctor-patient relationship
doctor_patient = Table(
    'doctor_patient',
    Base.metadata,
    Column('doctor_id', Integer, ForeignKey('doctors.id')),
    Column('patient_id', Integer, ForeignKey('patients.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'role'
    }

class Patient(User):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    phone_number = Column(String)
    address = Column(String)
    medical_history = Column(String)  # Store as JSON string
    allergies = Column(String)  # Store as JSON string
    current_medications = Column(String)  # Store as JSON string
    emergency_contact = Column(String)

    # Relationship with doctors
    doctors = relationship("Doctor", secondary=doctor_patient, back_populates="patients")
    # Relationship with appointments
    appointments = relationship("Appointment", back_populates="patient")

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
    }

class Doctor(User):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    specialization = Column(String)
    license_number = Column(String, unique=True)
    years_of_experience = Column(Integer)
    hospital_affiliation = Column(String)
    phone_number = Column(String)
    address = Column(String)
    consultation_fee = Column(Float)
    available_hours = Column(String)  # Store as JSON string
    calendar_id = Column(String, nullable=True)  # Google Calendar ID

    # Relationship with patients
    patients = relationship("Patient", secondary=doctor_patient, back_populates="doctors")
    # Relationship with appointments
    appointments = relationship("Appointment", back_populates="doctor")

    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
    }

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'))
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    google_event_id = Column(String, nullable=True)  # Store Google Calendar event ID

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments") 
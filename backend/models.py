from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Table, Text, Date
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

    # Add conversations relationship
    conversations = relationship("Conversation", back_populates="user")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'role'
    }

class Patient(User):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    date_of_birth = Column(Date)
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
    # Relationship with conversations
    conversations = relationship("Conversation", back_populates="user")

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

class VirtualAssistant(Base):
    __tablename__ = "virtual_assistants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Health Assistant")
    model_version = Column(String)
    capabilities = Column(String)  # Store as JSON string
    last_training_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with conversations
    conversations = relationship("Conversation", back_populates="agent")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    agent_id = Column(Integer, ForeignKey('virtual_assistants.id', ondelete='CASCADE'))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, completed, archived
    context = Column(String, nullable=True)  # Store as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="conversations")
    agent = relationship("VirtualAssistant", foreign_keys=[agent_id], back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id', ondelete='CASCADE'))
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    sender_type = Column(String)  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_type = Column(String)  # text, image, file, etc.
    message_metadata = Column(String, nullable=True)  # Store as JSON string

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])

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
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import logging
from pydantic import BaseModel, validator, ConfigDict

from database import get_db
from models import Conversation, Message, User, VirtualAssistant, Patient
from routers.auth import get_current_user

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)

# Pydantic models for request/response
class MessageBase(BaseModel):
    content: str
    message_type: str = "text"
    message_metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sender_id: Optional[int]
    sender_type: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

    @validator('message_metadata', pre=True)
    def parse_metadata(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        if hasattr(v, '__dict__'):
            return dict(v.__dict__)
        return v

class ConversationBase(BaseModel):
    context: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    agent_id: int
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

    @validator('context', pre=True)
    def parse_context(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        if hasattr(v, '__dict__'):
            return dict(v.__dict__)
        return v

    @validator('messages', pre=True)
    def parse_messages(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return [MessageResponse.from_orm(msg) for msg in v]
        return []

# Create a new conversation
@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify user is a patient
    if not isinstance(current_user, Patient):
        raise HTTPException(
            status_code=403,
            detail="Only patients can create conversations with the virtual assistant"
        )
    
    # Get the default virtual assistant
    agent = db.query(VirtualAssistant).filter(VirtualAssistant.is_active == True).first()
    if not agent:
        # Create default virtual assistant if none exists
        agent = VirtualAssistant(
            name="Health Assistant",
            model_version="1.0",
            capabilities=json.dumps(["health_consultation", "appointment_scheduling", "general_inquiry"])
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)

    # Create new conversation
    db_conversation = Conversation(
        user_id=current_user.id,
        agent_id=agent.id,
        context=json.dumps(conversation.context) if conversation.context else None
    )
    
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    # Log the conversation object for debugging
    logger.debug(f"Created conversation: {db_conversation.__dict__}")
    
    return db_conversation

# Get conversation history
@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .options(joinedload(Conversation.messages))
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")
    
    # Log the conversation object for debugging
    logger.debug(f"Retrieved conversation: {conversation.__dict__}")
    
    return conversation

# Get all conversations for the current user
@router.get("/my-conversations", response_model=List[ConversationResponse])
def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(Conversation)
        .options(joinedload(Conversation.messages))
        .filter(Conversation.user_id == current_user.id)
        .all()
    )
    
    # Log the conversations for debugging
    for conv in conversations:
        logger.debug(f"Retrieved conversation: {conv.__dict__}")
    
    return conversations

# Delete a conversation
@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this conversation")
    
    db.delete(conversation)
    db.commit()
    return None

# Add a message to a conversation
@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to send messages in this conversation")
    
    # Create new message
    db_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        sender_type='user',
        content=message.content,
        message_type=message.message_type,
        message_metadata=json.dumps(message.message_metadata) if message.message_metadata else None
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Log the message object for debugging
    logger.debug(f"Created message: {db_message.__dict__}")
    
    return db_message

# Delete a message
@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Verify user has access to this message
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")
    
    db.delete(message)
    db.commit()
    return None

# Update conversation status
@router.patch("/{conversation_id}/status", response_model=ConversationResponse)
def update_conversation_status(
    conversation_id: int,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .options(joinedload(Conversation.messages))
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this conversation")
    
    conversation.status = status
    if status == "completed":
        conversation.end_time = datetime.utcnow()
    
    db.commit()
    db.refresh(conversation)
    
    # Log the conversation object for debugging
    logger.debug(f"Updated conversation: {conversation.__dict__}")
    
    return conversation 
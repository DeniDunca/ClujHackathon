from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import get_db
from models import User
from routers.auth import get_current_active_user
from typing import Annotated, List
from pydantic import BaseModel

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

load_dotenv()  

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "documents"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class FileInfo(BaseModel):
    name: str
    created_at: str
    last_accessed_at: str
    size: int
    url: str

class DocumentUploader:
    def __init__(self, supabase_client: Client, bucket_name: str):
        self.supabase = supabase_client
        self.bucket = bucket_name

    def upload_file(self, file: UploadFile, user_id: int):
        try:
            file_content = file.file.read()
            # Create user-specific folder path
            user_folder = f"user_{user_id}"
            unique_filename = f"{user_folder}/{file.filename}"

            response = self.supabase.storage.from_(self.bucket).upload(
                unique_filename, file_content, {"content-type": file.content_type}
            )

            if not response:
                raise HTTPException(status_code=500, detail="Failed to upload file.")

            return {
                "filename": unique_filename,
                "message": "File uploaded successfully.",
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_user_files(self, user_id: int) -> List[FileInfo]:
        try:
            # List files in user's folder
            user_folder = f"user_{user_id}"
            files = self.supabase.storage.from_(self.bucket).list(user_folder)
            
            if not files:
                return []
            
            # Get file details and signed URLs
            file_info_list = []
            for file in files:
                file_path = f"{user_folder}/{file['name']}"
                # Get signed URL for file access
                signed_url = self.supabase.storage.from_(self.bucket).create_signed_url(
                    file_path, 60  # URL expires in 60 seconds
                )
                
                file_info = FileInfo(
                    name=file['name'],
                    created_at=file['created_at'],
                    last_accessed_at=file['last_accessed_at'],
                    size=file['metadata']['size'],
                    url=signed_url['signedURL']
                )
                file_info_list.append(file_info)
            
            return file_info_list
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

uploader = DocumentUploader(supabase, BUCKET_NAME)

@router.post("/")
async def upload(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Upload a document. Files are stored in user-specific folders.
    Requires authentication.
    """
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    
    return uploader.upload_file(file, current_user.id)

@router.get("/files", response_model=List[FileInfo])
async def get_user_files(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Get all files uploaded by the current user.
    Requires authentication.
    """
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    
    return uploader.get_user_files(current_user.id)

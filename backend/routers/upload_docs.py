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
import fitz
import tempfile
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    document_id: str
    original_file: dict
    text_file: dict
    created_at: str
    last_accessed_at: str

class DocumentUploader:
    def __init__(self, supabase_client: Client, bucket_name: str):
        self.supabase = supabase_client
        self.bucket = bucket_name

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        # Create a temporary file to store the PDF content
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf.write(file_content)
            temp_pdf_path = temp_pdf.name

        try:
            text = ""
            with fitz.open(temp_pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        finally:
            # Clean up the temporary file
            os.unlink(temp_pdf_path)

    def upload_file(self, file: UploadFile, user_id: int):
        try:
            file_content = file.file.read()
            
            # Create a unique folder for this document
            document_id = str(uuid.uuid4())
            user_folder = f"user_{user_id}"
            document_folder = f"{user_folder}/{document_id}"
            
            # Get original filename without extension
            original_name = os.path.splitext(file.filename)[0]
            
            # Upload original file
            original_filename = f"{document_folder}/{original_name}{os.path.splitext(file.filename)[1]}"
            response = self.supabase.storage.from_(self.bucket).upload(
                original_filename, file_content, {"content-type": file.content_type}
            )

            if not response:
                raise HTTPException(status_code=500, detail="Failed to upload original file.")

            # Extract text from PDF
            extracted_text = self.extract_text_from_pdf(file_content)
            
            # Create and upload text file with .txt extension
            text_filename = f"{document_folder}/{original_name}.txt"
            text_content = extracted_text.encode('utf-8')
            text_response = self.supabase.storage.from_(self.bucket).upload(
                text_filename, text_content, {"content-type": "text/plain"}
            )

            if not text_response:
                raise HTTPException(status_code=500, detail="Failed to upload text file.")

            # Get public URLs
            original_url = self.supabase.storage.from_(self.bucket).get_public_url(original_filename)
            text_url = self.supabase.storage.from_(self.bucket).get_public_url(text_filename)

            return {
                "document_id": document_id,
                "original_file": {
                    "filename": original_filename,
                    "url": str(original_url)
                },
                "text_file": {
                    "filename": text_filename,
                    "url": str(text_url)
                },
                "message": "Files uploaded successfully.",
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_user_files(self, user_id: int) -> List[FileInfo]:
        try:
            # List files in user's folder
            user_folder = f"user_{user_id}"
            logger.debug(f"Fetching files from folder: {user_folder}")
            
            # First, get the list of document folders
            folders = self.supabase.storage.from_(self.bucket).list(user_folder)
            logger.debug(f"Found folders: {folders}")
            
            if not folders:
                logger.debug("No folders found in user folder")
                return []
            
            # Group files by document folder
            document_files = {}
            
            # For each folder, get its contents
            for folder in folders:
                folder_name = folder['name']
                logger.debug(f"Processing folder: {folder_name}")
                
                # Get contents of this folder with the full path
                folder_path = f"{user_folder}/{folder_name}"
                logger.debug(f"Listing contents of: {folder_path}")
                folder_contents = self.supabase.storage.from_(self.bucket).list(folder_path)
                logger.debug(f"Folder contents: {folder_contents}")
                
                if not folder_contents:
                    continue
                
                document_files[folder_name] = {
                    'original_file': None,
                    'text_file': None,
                    'created_at': folder['created_at'] or folder_contents[0]['created_at'],
                    'last_accessed_at': folder['last_accessed_at'] or folder_contents[0]['last_accessed_at']
                }
                
                # Process each file in the folder
                for file in folder_contents:
                    filename = file['name']
                    logger.debug(f"Processing file: {filename}")
                    
                    # Determine if this is the original file or text file
                    if filename.endswith('.txt'):
                        logger.debug(f"Found text file: {filename}")
                        file_path = f"{folder_path}/{filename}"
                        signed_url = self.supabase.storage.from_(self.bucket).create_signed_url(file_path, 60)  # URL expires in 60 seconds
                        document_files[folder_name]['text_file'] = {
                            'filename': file_path,
                            'url': signed_url['signedURL']
                        }
                    else:
                        logger.debug(f"Found original file: {filename}")
                        file_path = f"{folder_path}/{filename}"
                        signed_url = self.supabase.storage.from_(self.bucket).create_signed_url(file_path, 60)  # URL expires in 60 seconds
                        document_files[folder_name]['original_file'] = {
                            'filename': file_path,
                            'url': signed_url['signedURL']
                        }
            
            logger.debug(f"Grouped document files: {document_files}")
            
            # Convert to list of FileInfo objects
            file_info_list = []
            for doc_id, files in document_files.items():
                # Include documents that have at least one file
                if files['original_file'] or files['text_file']:
                    logger.debug(f"Adding document: {doc_id}")
                    file_info = FileInfo(
                        document_id=doc_id,
                        original_file=files['original_file'],
                        text_file=files['text_file'],
                        created_at=files['created_at'],
                        last_accessed_at=files['last_accessed_at']
                    )
                    file_info_list.append(file_info)
                else:
                    logger.debug(f"Skipping empty document {doc_id}")
            
            logger.debug(f"Final file info list: {file_info_list}")
            return file_info_list
            
        except Exception as e:
            logger.error(f"Error in get_user_files: {str(e)}")
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

@router.get("/debug/list-all")
async def list_all_files(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Debug endpoint to list all files in the bucket.
    Requires authentication.
    """
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    
    try:
        # List all files in the bucket
        all_files = uploader.supabase.storage.from_(uploader.bucket).list()
        return {"files": all_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

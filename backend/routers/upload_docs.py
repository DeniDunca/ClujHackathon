from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from supabase import create_client, Client
import os
from dotenv import load_dotenv

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

load_dotenv()  

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "documents"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class DocumentUploader:
    def __init__(self, supabase_client: Client, bucket_name: str):
        self.supabase = supabase_client
        self.bucket = bucket_name

    def upload_file(self, file: UploadFile):
        try:
            file_content = file.file.read()
            unique_filename = f"{file.filename}"

            response = self.supabase.storage.from_(self.bucket).upload(
                unique_filename, file_content, {"content-type": file.content_type}
            )

            if not response:
                raise HTTPException(status_code=500, detail="Failed to upload file.")

            return {
                "filename": unique_filename,
                "message": "File uploaded successfully."
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


uploader = DocumentUploader(supabase, BUCKET_NAME)

@router.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return uploader.upload_file(file)

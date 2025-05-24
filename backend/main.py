from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import auth
from routers import upload_docs
from routers import patient
from routers import doctor
from routers import appointments
from routers import conversation

app = FastAPI(title="Healthonomics API")
models.Base.metadata.create_all(bind=engine)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def root():
    return FileResponse("static/test.html")

app.include_router(auth.router)
app.include_router(upload_docs.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointments.router)
app.include_router(conversation.router)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message received: {data}")
#     except:
#         await websocket.close()

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
from routers import auth

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def root():
    return FileResponse("static/test.html")

app.include_router(auth.router)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message received: {data}")
#     except:
#         await websocket.close()

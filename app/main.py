from fastapi import FastAPI
from app.routes import stream_routes
from app.routes.uploadEcg_routes import router as upload_router
from dotenv import load_dotenv

try:
    load_dotenv(".env")
except Exception:
    pass

app = FastAPI()

app.include_router(stream_routes.router)
app.include_router(upload_router)

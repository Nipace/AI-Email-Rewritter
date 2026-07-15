from fastapi import FastAPI
from dotenv import load_dotenv

import os
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if frontend_url:
    allowed_origins.append(frontend_url.rstrip("/"))
    
print("Allowed CORS origins:", allowed_origins)    
app = FastAPI(
    title="AI Email Rewriter API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
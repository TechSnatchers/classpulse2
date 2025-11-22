from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os
from contextlib import asynccontextmanager
from src.middleware.auth import AuthMiddleware
from src.database.connection import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.vercel.app",
        "https://zoomlearningapp.de",
        "https://www.zoomlearningapp.de",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_middleware = AuthMiddleware()

@app.middleware("http")
async def auth_middleware_wrapper(request: Request, call_next):
    # Bypass auth for Zoom webhook
    if request.url.path.startswith("/api/zoom/webhook"):
        return await call_next(request)
    return await auth_middleware(request, call_next)

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    # Skip CSP for Zoom webhook
    if request.url.path.startswith("/api/zoom/webhook"):
        return await call_next(request)

    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

# ------------------------
# Routes
# ------------------------
from src.routers import (
    auth, quiz, clustering, question,
    zoom_webhook, zoom_chatbot, course, live_question
)

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(clustering.router)
app.include_router(question.router)
app.include_router(zoom_webhook.router)
app.include_router(zoom_chatbot.router)
app.include_router(course.router)
app.include_router(live_question.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


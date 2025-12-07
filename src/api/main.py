"""FastAPI application for AgentKit."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import generate, tools

app = FastAPI(
    title="AgentKit",
    description="Generate backend tools for AI agents",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router, tags=["generate"])
app.include_router(tools.router, tags=["tools"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "AgentKit",
        "status": "running",
        "description": "Generate backend tools for AI agents with Gemini 3 Pro",
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}

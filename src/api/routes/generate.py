"""Generation endpoint with SSE streaming."""

import json
import asyncio
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from src.core.schemas import GenerateRequest
from src.generator import generate_tool

router = APIRouter()


async def generation_stream(request: GenerateRequest):
    """Stream generation progress as SSE events."""
    try:
        # Planning event
        yield {
            "event": "planning",
            "data": json.dumps({
                "step": "Analyzing requirements",
                "description": request.description,
                "requirements": request.requirements,
            })
        }
        await asyncio.sleep(0.5)

        # Generating event
        yield {
            "event": "generating",
            "data": json.dumps({
                "step": "Generating code with Gemini 3 Pro",
                "progress": 0.3,
            })
        }

        # Actually generate the tool
        project_id, tool = await generate_tool(
            description=request.description,
            name=request.name,
            requirements=request.requirements,
        )

        # Progress update
        yield {
            "event": "generating",
            "data": json.dumps({
                "step": "Writing files",
                "progress": 0.8,
            })
        }
        await asyncio.sleep(0.3)

        # Complete event
        yield {
            "event": "complete",
            "data": json.dumps({
                "project_id": project_id,
                "name": tool.name,
                "description": tool.description,
                "tools": tool.tools,
                "files": [f.path for f in tool.files],
            })
        }

    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e)})
        }


@router.post("/generate")
async def generate(request: GenerateRequest):
    """Generate a new agent tool with SSE streaming."""
    return EventSourceResponse(generation_stream(request))


@router.post("/generate/sync")
async def generate_sync(request: GenerateRequest):
    """Generate a new agent tool (synchronous, non-streaming)."""
    try:
        project_id, tool = await generate_tool(
            description=request.description,
            name=request.name,
            requirements=request.requirements,
        )
        return {
            "project_id": project_id,
            "name": tool.name,
            "description": tool.description,
            "tools": tool.tools,
            "files": [f.path for f in tool.files],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

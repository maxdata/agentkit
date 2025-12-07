"""Tools management endpoints."""

from fastapi import APIRouter, HTTPException

from src.generator import get_project, list_projects, get_schema
from src.core.schemas import SchemaFormat

router = APIRouter()


@router.get("/tools")
async def list_all_tools():
    """List all generated tools."""
    return {"tools": list_projects()}


@router.get("/tools/{project_id}")
async def get_tool(project_id: str):
    """Get details of a generated tool."""
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tool = project["tool"]
    return {
        "project_id": project_id,
        "name": tool.name,
        "description": tool.description,
        "tools": tool.tools,
        "files": [f.path for f in tool.files],
        "created_at": project["created_at"],
        "path": project["path"],
    }


@router.get("/tools/{project_id}/schema/{format}")
async def get_tool_schema(project_id: str, format: SchemaFormat):
    """Get agent schema for a tool in specified format."""
    schema = get_schema(project_id, format.value)
    if not schema:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "format": format.value,
        "schema": schema,
    }

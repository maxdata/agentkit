"""Tool generation engine."""

import os
import re
import uuid
from pathlib import Path
from datetime import datetime

from src.core.gemini import generate_tool_code
from src.core.schemas import GeneratedTool, GeneratedFile


# In-memory storage for generated projects
_projects: dict[str, dict] = {}


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]


async def generate_tool(
    description: str,
    name: str | None = None,
    requirements: list[str] | None = None,
    output_dir: str = "generated",
) -> tuple[str, GeneratedTool]:
    """Generate a complete agent tool.

    Returns:
        Tuple of (project_id, GeneratedTool)
    """
    # Generate name from description if not provided
    if not name:
        words = description.split()[:3]
        name = slugify("-".join(words))

    # Generate code with Gemini
    result = generate_tool_code(
        description=description,
        name=name,
        requirements=requirements or [],
    )

    # Create project directory
    project_id = str(uuid.uuid4())[:8]
    project_dir = Path(output_dir) / f"{name}-{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    files = []
    for file_data in result.get("files", []):
        file_path = project_dir / file_data["path"]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file_data["content"])
        files.append(GeneratedFile(path=str(file_path), content=file_data["content"]))

    # Create tool object
    tool = GeneratedTool(
        name=result.get("tool_name", name),
        description=result.get("tool_description", description),
        tools=result.get("functions", []),
        files=files,
    )

    # Store in memory
    _projects[project_id] = {
        "tool": tool,
        "created_at": datetime.now().isoformat(),
        "path": str(project_dir),
    }

    return project_id, tool


def get_project(project_id: str) -> dict | None:
    """Get a stored project by ID."""
    return _projects.get(project_id)


def list_projects() -> list[dict]:
    """List all generated projects."""
    return [
        {
            "project_id": pid,
            "name": data["tool"].name,
            "description": data["tool"].description,
            "created_at": data["created_at"],
            "path": data["path"],
        }
        for pid, data in _projects.items()
    ]


def get_schema(project_id: str, format: str) -> dict | None:
    """Get agent schema for a project in specified format."""
    project = get_project(project_id)
    if not project:
        return None

    tool = project["tool"]
    functions = tool.tools

    if format == "openai":
        return {
            "functions": [
                {
                    "name": f["name"],
                    "description": f["description"],
                    "parameters": f["parameters"],
                }
                for f in functions
            ]
        }
    elif format == "claude":
        return {
            "tools": [
                {
                    "name": f["name"],
                    "description": f["description"],
                    "input_schema": f["parameters"],
                }
                for f in functions
            ]
        }
    elif format == "gemini":
        return {
            "function_declarations": [
                {
                    "name": f["name"],
                    "description": f["description"],
                    "parameters": f["parameters"],
                }
                for f in functions
            ]
        }
    elif format == "combined":
        return {
            "openai": get_schema(project_id, "openai"),
            "claude": get_schema(project_id, "claude"),
            "gemini": get_schema(project_id, "gemini"),
        }

    return None

"""Pydantic models for AgentKit."""

from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class GenerateRequest(BaseModel):
    """Request to generate a new agent tool."""
    description: str = Field(..., description="Natural language description of the tool")
    name: str | None = Field(None, description="Optional name for the tool (auto-generated if not provided)")
    requirements: list[str] = Field(default_factory=list, description="Additional requirements")


class GeneratedFile(BaseModel):
    """A generated file."""
    path: str
    content: str


class GeneratedTool(BaseModel):
    """A fully generated tool."""
    name: str
    description: str
    tools: list[dict]  # List of tool/function definitions
    files: list[GeneratedFile]


class SchemaFormat(str, Enum):
    """Supported agent schema formats."""
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    COMBINED = "combined"


class SSEEvent(BaseModel):
    """Server-sent event."""
    event: Literal["planning", "generating", "complete", "error"]
    data: dict


class ToolInfo(BaseModel):
    """Basic tool information."""
    name: str
    description: str
    tools: list[dict]
    created_at: str


class ProjectStorage(BaseModel):
    """Storage for generated projects."""
    projects: dict[str, GeneratedTool] = Field(default_factory=dict)

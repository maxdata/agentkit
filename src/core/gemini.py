"""Gemini 3 Pro client for code generation."""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


def get_client() -> genai.Client:
    """Get Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")
    return genai.Client(api_key=api_key)


def generate_tool_code(description: str, name: str, requirements: list[str]) -> dict:
    """Generate complete tool code using Gemini 3 Pro."""
    client = get_client()

    requirements_str = "\n".join(f"- {r}" for r in requirements) if requirements else "None specified"

    prompt = f"""You are a senior backend engineer. Generate a complete agent tool based on this description.

TOOL NAME: {name}
DESCRIPTION: {description}
ADDITIONAL REQUIREMENTS:
{requirements_str}

Generate a complete, working tool with:
1. FastAPI backend with proper routes
2. Function schemas for OpenAI, Claude, and Gemini formats
3. MCP server for Claude Desktop integration

Output valid JSON with this exact structure:
{{
    "tool_name": "{name}",
    "tool_description": "one line description",
    "functions": [
        {{
            "name": "function_name",
            "description": "what it does",
            "parameters": {{
                "type": "object",
                "properties": {{
                    "param1": {{"type": "string", "description": "..."}}
                }},
                "required": ["param1"]
            }}
        }}
    ],
    "files": [
        {{
            "path": "src/api/main.py",
            "content": "# full file content here"
        }},
        {{
            "path": "src/api/routes/{name}.py",
            "content": "# routes code"
        }},
        {{
            "path": "src/core/{name}.py",
            "content": "# business logic"
        }},
        {{
            "path": "agent_schemas/openai_functions.json",
            "content": "{{...}}"
        }},
        {{
            "path": "agent_schemas/claude_tools.json",
            "content": "{{...}}"
        }},
        {{
            "path": "agent_schemas/gemini_declarations.json",
            "content": "{{...}}"
        }},
        {{
            "path": "mcp/server.py",
            "content": "# MCP server code"
        }},
        {{
            "path": "pyproject.toml",
            "content": "# project config"
        }},
        {{
            "path": "README.md",
            "content": "# readme"
        }}
    ]
}}

Requirements for generated code:
- FastAPI with proper error handling and type hints
- Pydantic models for validation
- Each function should be atomic and focused
- Schema descriptions optimized for AI agent comprehension
- MCP server using the mcp library
- Include a pyproject.toml with dependencies
- Include a README with usage instructions

Return ONLY valid JSON, no markdown code blocks."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=8192,
        ),
    )

    # Parse response
    text = response.text.strip()

    # Remove markdown code blocks if present
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

    return json.loads(text)


def analyze_code(code: str) -> dict:
    """Analyze generated code for issues using Gemini."""
    client = get_client()

    prompt = f"""Analyze this code for issues:

```python
{code}
```

Return JSON with:
{{
    "score": 0-100,
    "issues": [
        {{"severity": "high|medium|low", "message": "...", "line": 1}}
    ],
    "suggestions": ["..."]
}}

Return ONLY valid JSON."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=2048,
        ),
    )

    text = response.text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

    return json.loads(text)

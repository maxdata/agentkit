# AgentKit - Specification

## Overview

Generate backend tools for AI agents. Describe what tool you need, get a complete backend with agent-ready function schemas for Claude, Gemini, and OpenAI.

**Category**: Technology
**Stack**: Gemini Python SDK + Claude Agent SDK + FastAPI

---

## Problem Statement

AI agents need tools to be useful. But creating tools for agents requires:
- Writing the backend API
- Creating function schemas for each agent format (OpenAI, Claude, Gemini)
- Testing that agents can actually call the tools
- Maintaining multiple schema formats

Developers spend more time on plumbing than on the actual tool logic.

## Solution

AgentKit generates complete, agent-ready backends:
1. Describe the tool you need in natural language
2. Gemini generates the backend + all agent schemas
3. Get a ready-to-use tool that any AI agent can call
4. Includes MCP server for Claude Desktop integration

---

## User Stories

1. As a developer, I want to describe a tool and get agent-ready code
2. As a developer, I want function schemas for Claude, Gemini, and OpenAI
3. As a developer, I want an MCP server for Claude Desktop
4. As an AI agent, I want to generate my own tools on-the-fly
5. As a developer, I want the generated code analyzed and improved automatically

---

## Features

### MVP (Competition)

| Feature | Priority | Description |
|---------|----------|-------------|
| Natural Language Input | P0 | Describe tool in plain English |
| Backend Generation | P0 | FastAPI backend with endpoints |
| Agent Schemas | P0 | Claude, Gemini, OpenAI function formats |
| MCP Server | P0 | Claude Desktop integration |
| Code Analysis | P1 | Scan for issues, auto-improve |
| CLI Access | P1 | Generate tools from command line |

### Future

- Tool chaining (multi-tool workflows)
- Agent testing harness
- Tool marketplace
- Version management

---

## Generated Project Structure

**Input**: "A weather tool that gets current weather and forecasts for any city"

**Output**:
```
generated/weather-tool/
├── README.md
├── pyproject.toml
├── .env.example
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/                      # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       └── weather.py        # GET /weather, GET /forecast
│   │
│   ├── core/                     # Business logic
│   │   ├── __init__.py
│   │   └── weather.py            # Weather API client
│   │
│   └── config.py
│
├── agent_schemas/                # Agent-ready function definitions
│   ├── openai_functions.json     # OpenAI function calling format
│   ├── claude_tools.json         # Claude tool use format
│   ├── gemini_declarations.json  # Gemini function declarations
│   └── combined.json             # All formats in one file
│
├── mcp/                          # Claude Desktop integration
│   ├── __init__.py
│   ├── server.py                 # MCP server implementation
│   └── claude_desktop_config.json
│
└── tests/
    └── test_weather.py
```

---

## Agent Schema Formats

### OpenAI Functions (openai_functions.json)
```json
{
  "functions": [
    {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "City name, e.g. 'Tokyo' or 'New York'"
          },
          "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "Temperature units"
          }
        },
        "required": ["city"]
      }
    },
    {
      "name": "get_forecast",
      "description": "Get weather forecast for next N days",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"},
          "days": {"type": "integer", "minimum": 1, "maximum": 7}
        },
        "required": ["city", "days"]
      }
    }
  ]
}
```

### Claude Tools (claude_tools.json)
```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "input_schema": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "City name, e.g. 'Tokyo' or 'New York'"
          },
          "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["city"]
      }
    }
  ]
}
```

### Gemini Function Declarations (gemini_declarations.json)
```json
{
  "function_declarations": [
    {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "City name"
          },
          "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["city"]
      }
    }
  ]
}
```

---

## API Endpoints

### POST /generate

Generate agent tool from description.

**Request**:
```json
{
  "description": "A weather tool that gets current weather and forecasts",
  "requirements": ["OpenWeatherMap API", "celsius and fahrenheit"],
  "name": "weather-tool"
}
```

**Response** (SSE):
```
event: planning
data: {"step": "Analyzing requirements", "tools": ["get_weather", "get_forecast"]}

event: generating
data: {"file": "src/api/routes/weather.py", "progress": 0.3}

event: generating
data: {"file": "agent_schemas/claude_tools.json", "progress": 0.6}

event: generating
data: {"file": "mcp/server.py", "progress": 0.8}

event: complete
data: {
  "project_id": "uuid",
  "name": "weather-tool",
  "tools": [
    {"name": "get_weather", "description": "Get current weather"},
    {"name": "get_forecast", "description": "Get forecast"}
  ],
  "schemas": ["openai", "claude", "gemini"],
  "mcp_ready": true
}
```

### GET /tools/{project_id}/schema/{format}

Get agent schema in specific format.

**Formats**: `openai`, `claude`, `gemini`, `combined`

**Response**:
```json
{
  "format": "claude",
  "tools": [...]
}
```

### POST /tools/{project_id}/test

Test tool with sample agent call.

**Request**:
```json
{
  "tool": "get_weather",
  "input": {"city": "Tokyo", "units": "celsius"}
}
```

**Response**:
```json
{
  "success": true,
  "output": {
    "city": "Tokyo",
    "temperature": 22,
    "condition": "Partly cloudy",
    "humidity": 65
  },
  "latency_ms": 230
}
```

---

## CLI Commands

```bash
# Generate agent tool
agentkit generate "A calculator with basic math operations"
agentkit generate "A file search tool" --name file-search

# Get schemas
agentkit schema <project-id> --format claude
agentkit schema <project-id> --format openai
agentkit schema <project-id> --format all

# Test tool
agentkit test <project-id> --tool get_weather --input '{"city": "Tokyo"}'

# Start MCP server (for Claude Desktop)
agentkit mcp <project-id> --port 3000

# List generated tools
agentkit list
```

---

## MCP Server Integration

Generated tools include an MCP server for Claude Desktop:

```python
# mcp/server.py
from mcp import Server, Tool

server = Server("weather-tool")

@server.tool()
async def get_weather(city: str, units: str = "celsius") -> dict:
    """Get current weather for a city."""
    # ... implementation
    return {"city": city, "temperature": 22, "condition": "Sunny"}

@server.tool()
async def get_forecast(city: str, days: int) -> dict:
    """Get weather forecast for next N days."""
    # ... implementation
    return {"city": city, "forecast": [...]}

if __name__ == "__main__":
    server.run()
```

**Claude Desktop config** (claude_desktop_config.json):
```json
{
  "mcpServers": {
    "weather-tool": {
      "command": "python",
      "args": ["-m", "mcp.server"],
      "cwd": "/path/to/generated/weather-tool"
    }
  }
}
```

---

## Demo Flow

**2-minute competition demo:**

1. **[0:00]** "AgentKit - generate tools for AI agents"

2. **[0:15]** Describe tool:
   ```
   agentkit generate "A bookmark manager with add, search, and tag operations"
   ```

3. **[0:30]** Show generated files:
   - FastAPI backend
   - Claude/Gemini/OpenAI schemas
   - MCP server

4. **[0:45]** Start the tool:
   ```
   uvicorn src.api.main:app
   ```

5. **[1:00]** Claude agent uses the tool:
   ```python
   import anthropic

   client = anthropic.Anthropic()
   tools = json.load(open("agent_schemas/claude_tools.json"))

   response = client.messages.create(
       model="claude-sonnet-4-20250514",
       tools=tools["tools"],
       messages=[{"role": "user", "content": "Add bookmark for github.com with tag 'dev'"}]
   )
   # Claude calls the generated tool!
   ```

6. **[1:30]** Show tool being called, response returned

7. **[1:50]** "AgentKit - agents can build their own tools"

---

## Gemini Prompt Strategy

### Tool Generation System Prompt

```
You are a senior backend engineer specializing in AI agent tools.

Given a natural language description, generate:
1. FastAPI backend with proper routes
2. Function schemas for OpenAI, Claude, and Gemini formats
3. MCP server for Claude Desktop integration
4. Pydantic models for validation

Requirements:
- Each tool function should be atomic and focused
- Include proper error handling
- Add type hints everywhere
- Schema descriptions should be clear for AI agents
- Follow each platform's exact schema format

Output JSON with all file paths and contents.
```

### Schema Generation Prompt

```
Convert this API endpoint to agent function schemas:

Endpoint: {endpoint}
Method: {method}
Parameters: {params}
Response: {response}

Generate schemas for:
1. OpenAI function calling format
2. Claude tool use format
3. Gemini function declarations format

Ensure descriptions are optimized for AI agent comprehension.
```

---

## Architecture

```
agentkit/
├── spec.md
├── pyproject.toml
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/                      # AgentKit API
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── generate.py       # POST /generate
│   │       ├── tools.py          # GET /tools, /schema
│   │       └── test.py           # POST /test
│   │
│   ├── cli/                      # CLI interface
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── generator/                # Tool generation engine
│   │   ├── __init__.py
│   │   ├── planner.py            # Analyze requirements
│   │   ├── backend_gen.py        # Generate FastAPI code
│   │   ├── schema_gen.py         # Generate agent schemas
│   │   ├── mcp_gen.py            # Generate MCP server
│   │   └── prompts.py
│   │
│   ├── analyzer/                 # Code analysis
│   │   ├── __init__.py
│   │   └── scanner.py
│   │
│   └── core/
│       ├── __init__.py
│       ├── gemini.py             # Gemini Python SDK client
│       ├── storage.py
│       └── schemas.py
│
├── generated/                    # Output folder
│
└── tests/
```

---

## Example: Agent Building Its Own Tool

```python
# An agent that creates tools for itself using AgentKit

from anthropic import Anthropic
import requests

client = Anthropic()

# Agent realizes it needs a new tool
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{
        "role": "user",
        "content": "I need to track my expenses. Create a tool for that."
    }]
)

# Agent calls AgentKit to generate the tool
agentkit_response = requests.post(
    "http://localhost:8000/generate",
    json={
        "description": "Expense tracker with add, list, and summarize operations",
        "requirements": ["categories", "date filtering", "monthly totals"]
    }
)

# Now the agent has a new tool it can use!
new_tools = requests.get(
    f"http://localhost:8000/tools/{project_id}/schema/claude"
).json()

# Agent uses its newly created tool
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    tools=new_tools["tools"],
    messages=[{"role": "user", "content": "Add expense: $50 for lunch, category: food"}]
)
```

---

## Why This Wins

1. **Unique angle**: Agents creating tools for agents
2. **Heavy Gemini usage**: Generation, analysis, schema creation
3. **Multi-agent demo**: Gemini generates, Claude uses
4. **Practical output**: Real tools that actually work
5. **MCP integration**: Claude Desktop ready
6. **Clear story**: "What if agents could build their own tools?"

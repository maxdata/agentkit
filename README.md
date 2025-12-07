# AgentKit

Generate backend tools for AI agents with Gemini 3 Pro. Describe what tool you need, get a complete backend with agent-ready function schemas for Claude, Gemini, and OpenAI.

## Quick Start

```bash
# Install
pip install -e .

# Set your Gemini API key
export GEMINI_API_KEY=your_key_here

# Generate a tool
agentkit generate "A todo list with add, complete, and list tasks"
```

## Features

- **Natural Language Input**: Describe your tool in plain English
- **Complete Backend**: FastAPI server with proper endpoints
- **Multi-Platform Schemas**: Claude, Gemini, and OpenAI function formats
- **MCP Server**: Claude Desktop integration out of the box
- **Powered by Gemini 3 Pro**: Fast, intelligent code generation

## Usage

### CLI

```bash
# Generate a tool
agentkit generate "A weather tool that gets forecasts"
agentkit generate "A bookmark manager" --name bookmarks

# List generated tools
agentkit list

# Get schema for a tool
agentkit schema <project-id> --format claude
agentkit schema <project-id> --format openai
agentkit schema <project-id> --format combined

# Get tool info
agentkit info <project-id>
```

### API

```bash
# Start the server
uvicorn src.api.main:app --reload

# Generate a tool (SSE streaming)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "A calculator with basic operations"}'

# List tools
curl http://localhost:8000/tools

# Get schema
curl http://localhost:8000/tools/{project_id}/schema/claude
```

## Generated Output

When you generate a tool, AgentKit creates:

```
generated/your-tool-abc123/
├── src/
│   ├── api/
│   │   ├── main.py           # FastAPI server
│   │   └── routes/
│   └── core/                 # Business logic
├── agent_schemas/
│   ├── openai_functions.json
│   ├── claude_tools.json
│   └── gemini_declarations.json
├── mcp/
│   └── server.py             # Claude Desktop MCP server
├── pyproject.toml
└── README.md
```

## Using Generated Tools

### With Claude

```python
import anthropic
import json

client = anthropic.Anthropic()
tools = json.load(open("generated/todo-abc123/agent_schemas/claude_tools.json"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    tools=tools["tools"],
    messages=[{"role": "user", "content": "Add a task: finish the project"}]
)
```

### With OpenAI

```python
import openai
import json

client = openai.OpenAI()
functions = json.load(open("generated/todo-abc123/agent_schemas/openai_functions.json"))

response = client.chat.completions.create(
    model="gpt-4",
    functions=functions["functions"],
    messages=[{"role": "user", "content": "Add a task: finish the project"}]
)
```

### With Claude Desktop (MCP)

```bash
# Start the MCP server
cd generated/todo-abc123
python -m mcp.server

# Add to Claude Desktop config
# See generated/todo-abc123/mcp/claude_desktop_config.json
```

## Development

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/agentkit.git
cd agentkit
pip install -e ".[dev]"

# Run tests
pytest

# Start dev server
uvicorn src.api.main:app --reload
```

## How It Works

1. **You describe** the tool you want in natural language
2. **Gemini 3 Pro analyzes** your requirements and plans the tool structure
3. **Gemini generates** complete, working code:
   - FastAPI backend with endpoints
   - Pydantic models for validation
   - Function schemas for all major AI agent platforms
   - MCP server for Claude Desktop
4. **You get** a ready-to-use tool that any AI agent can call

## License

MIT

---

Built with Gemini 3 Pro for the [Kaggle Vibe Code Competition](https://www.kaggle.com/competitions/gemini-3)

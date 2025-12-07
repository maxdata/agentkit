# Agent Tools - Implementation Plan

## Phase 1: Setup

### Step 1.1: Project Structure
```
agent-tools/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   └── functions/
│       └── definitions.py
├── tests/
├── requirements.txt
└── pyproject.toml
```

### Step 1.2: Dependencies
```
fastapi
uvicorn
sse-starlette
typer
rich
httpx
pydantic
agent-core  # local dependency
```

## Phase 2: API

### Step 2.1: FastAPI App
Prompt:
```
Create a FastAPI application with these endpoints:

POST /generate
- Accept: {"type": "api|cli", "description": "...", "requirements": [...]}
- Return SSE stream with planning and code events
- Use agent-core generator

POST /evaluate
- Accept: {"project_id": "uuid"}
- Return: {"score": 85, "checks": {...}, "suggestions": [...]}
- Use agent-core evaluator

POST /improve
- Accept: {"project_id": "uuid", "request": "..."}
- Return: {"changes": [...], "new_score": 92}
- Use agent-core improver

Include CORS, error handling, Pydantic models.
```

### Step 2.2: SSE Streaming
Prompt:
```
Implement SSE streaming for /generate endpoint:

Events:
- planning: {"step": "...", "details": "..."}
- code: {"file": "...", "content": "...", "progress": 0.5}
- complete: {"project_id": "uuid", "files": [...]}

Use sse-starlette for streaming.
Handle client disconnection gracefully.
```

## Phase 3: CLI

### Step 3.1: Typer CLI
Prompt:
```
Create a Typer CLI with these commands:

agent-tools generate --type api --desc "..." [--requirements ...]
- Calls API /generate endpoint
- Shows progress with Rich
- Saves files to disk

agent-tools evaluate --project-id <uuid>
- Calls API /evaluate endpoint
- Pretty-prints results with colors

agent-tools improve --project-id <uuid> --request "..."
- Calls API /improve endpoint
- Shows diff of changes

agent-tools loop --type cli --desc "..." --target-score 90
- Full loop: generate -> evaluate -> improve until target
- Shows progress throughout
```

### Step 3.2: Rich Output
Prompt:
```
Add Rich formatting to CLI:
- Progress bars for generation
- Tables for evaluation results
- Colored severity badges
- Syntax-highlighted code diffs
- Spinners for waiting states
```

## Phase 4: Agent Functions

### Step 4.1: Function Definitions
Prompt:
```
Create function definitions for AI agents:

generate_code:
- description: "Generate API or CLI code from description"
- parameters: code_type, description, requirements

evaluate_code:
- description: "Run quality checks on generated code"
- parameters: project_id

improve_code:
- description: "Apply improvements to generated code"
- parameters: project_id, request

Output as JSON Schema compatible with OpenAI/Claude tools.
```

---

## Validation Checklist

### API
- [ ] POST /generate streams SSE events
- [ ] POST /evaluate returns score and checks
- [ ] POST /improve returns changes
- [ ] CORS configured for frontend
- [ ] Error responses are proper JSON
- [ ] Project storage works

### CLI
- [ ] generate command works
- [ ] evaluate command works
- [ ] improve command works
- [ ] loop command iterates correctly
- [ ] Rich output looks good
- [ ] Errors handled gracefully

### Agent Functions
- [ ] JSON Schema is valid
- [ ] Compatible with OpenAI function calling
- [ ] Compatible with Claude tools
- [ ] All parameters documented

---

## Prompts Archive

### Complete API Prompt
```
Create a complete FastAPI application for agent tools.

File: src/api/main.py

Endpoints:

1. POST /generate (SSE)
   Request: {"type": "api|cli", "description": "...", "requirements": [...]}
   Stream events: planning, code, complete

2. POST /evaluate
   Request: {"project_id": "uuid"}
   Response: {"score": int, "checks": {...}, "suggestions": [...]}

3. POST /improve
   Request: {"project_id": "uuid", "request": "..."}
   Response: {"changes": [...], "new_score": int}

Include:
- Pydantic models for all requests/responses
- CORS middleware
- Error handling with HTTPException
- In-memory project storage (dict)
- Integration with agent-core module

Make it production-ready.
```

### Complete CLI Prompt
```
Create a complete Typer CLI for agent tools.

File: src/cli/main.py

Commands:

1. generate
   Options: --type (api/cli), --desc (string), --requirements (list)
   Behavior: Call API, show progress, save files

2. evaluate
   Options: --project-id (uuid)
   Behavior: Call API, display results table

3. improve
   Options: --project-id (uuid), --request (string)
   Behavior: Call API, show diff

4. loop
   Options: --type, --desc, --target-score (int)
   Behavior: Generate, evaluate, improve until target

Use Rich for:
- Progress bars
- Tables
- Colored output
- Syntax highlighting
- Spinners

Handle API errors gracefully.
```

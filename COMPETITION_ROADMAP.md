# AgentKit Competition Roadmap

## Competition Info
- **Deadline:** December 12, 2025 (5 days from now)
- **Prize:** $500,000 in Gemini API credits (Top 50 get $10,000 each)
- **Judging:** 40% real-world impact, 30% Gemini 3 Pro usage, 30% other

---

## Current Status

| Item | Status |
|------|--------|
| Spec document | ✅ Done |
| Plan document | ✅ Done |
| Writeup draft | ✅ Done |
| **Core code** | ❌ Not started |
| **API** | ❌ Not started |
| **CLI** | ❌ Not started |
| **Demo video** | ❌ Not started |
| **Kaggle submission** | ❌ Not started |

---

## Step-by-Step Roadmap

### Phase 1: Setup (30 min)

#### Step 1.1: Create project structure
```bash
cd gemini-competition/agentkit
mkdir -p src/{api/routes,cli,generator,core}
mkdir -p generated tests
touch src/__init__.py src/api/__init__.py src/cli/__init__.py
touch src/generator/__init__.py src/core/__init__.py
```

#### Step 1.2: Create pyproject.toml
```toml
[project]
name = "agentkit"
version = "0.1.0"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "sse-starlette>=1.8.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.25.0",
    "pydantic>=2.5.0",
    "google-genai>=1.0.0",
]

[project.scripts]
agentkit = "src.cli.main:app"
```

#### Step 1.3: Get Gemini API key
1. Go to https://aistudio.google.com/
2. Get API key
3. Create `.env` with `GEMINI_API_KEY=your_key`

---

### Phase 2: Core Generator (2-3 hours)

#### Step 2.1: Gemini client (`src/core/gemini.py`)
- Initialize Gemini 3 Pro client
- Create generation function with structured output

#### Step 2.2: Backend generator (`src/generator/backend_gen.py`)
- Prompt Gemini to generate FastAPI code
- Parse response into files
- Write files to disk

#### Step 2.3: Schema generator (`src/generator/schema_gen.py`)
- Generate OpenAI function schema
- Generate Claude tool schema
- Generate Gemini function declaration

#### Step 2.4: MCP generator (`src/generator/mcp_gen.py`)
- Generate MCP server code for Claude Desktop

---

### Phase 3: API (1-2 hours)

#### Step 3.1: FastAPI app (`src/api/main.py`)
- CORS middleware
- Health check endpoint

#### Step 3.2: Generate route (`src/api/routes/generate.py`)
- POST /generate
- SSE streaming (planning → generating → complete)
- Return project_id and file list

#### Step 3.3: Tools route (`src/api/routes/tools.py`)
- GET /tools/{project_id}
- GET /tools/{project_id}/schema/{format}

---

### Phase 4: CLI (1 hour)

#### Step 4.1: Typer CLI (`src/cli/main.py`)
```bash
agentkit generate "description here"
agentkit list
agentkit schema <id> --format claude
```

#### Step 4.2: Rich output
- Progress bars during generation
- Pretty print results

---

### Phase 5: Testing (1 hour)

#### Step 5.1: Test generation flow
```bash
# Start server
uvicorn src.api.main:app --reload

# Test CLI
agentkit generate "A todo list with add, complete, and list tasks"
```

#### Step 5.2: Test generated tool
```bash
cd generated/todo-tool
uvicorn src.api.main:app --port 8001

# Verify endpoints work
curl http://localhost:8001/tasks
```

#### Step 5.3: Test with Claude
```python
import anthropic
import json

client = anthropic.Anthropic()
tools = json.load(open("generated/todo-tool/agent_schemas/claude_tools.json"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    tools=tools["tools"],
    messages=[{"role": "user", "content": "Add task: finish competition"}]
)
```

---

### Phase 6: Demo Video (1-2 hours)

#### Step 6.1: Script (2 minutes max)
```
[0:00-0:10] "AgentKit - generate tools for AI agents instantly"

[0:10-0:30] Show the problem
- "Building agent tools requires writing backend code, schemas for each platform..."
- "That's hours of boilerplate"

[0:30-1:00] Run AgentKit
- Terminal: agentkit generate "A bookmark manager with add, search, and tag"
- Show generation progress
- Show generated files

[1:00-1:30] Test the tool
- Start the generated server
- Claude calls the tool successfully
- Show the response

[1:30-1:50] Key features
- "Works with Claude, Gemini, and OpenAI"
- "Includes MCP server for Claude Desktop"
- "Powered by Gemini 3 Pro"

[1:50-2:00] Close
- "AgentKit - agents can build their own tools"
- Show GitHub link
```

#### Step 6.2: Record
- Use OBS, Loom, or QuickTime
- Record terminal + code editor
- Keep it under 2 minutes

#### Step 6.3: Upload
- YouTube (unlisted) or direct upload to Kaggle

---

### Phase 7: Submit (30 min)

#### Step 7.1: Push code to GitHub
```bash
git add .
git commit -m "AgentKit - Gemini 3 competition submission"
git push origin main
```

#### Step 7.2: Submit on Kaggle
1. Go to https://www.kaggle.com/competitions/gemini-3/writeups
2. Create new writeup
3. Fill in:
   - **Title:** AgentKit - Generate Backend Tools for AI Agents
   - **Category:** Technology
   - **Summary:** (from writeup.md)
   - **Video:** Link to demo
   - **GitHub:** Link to repo
4. Copy content from `writeup.md`
5. Submit

---

## Winning Tips

### Maximize Impact Score (40%)
- Show real-world use case (developers saving hours)
- Demonstrate working end-to-end flow
- Show multi-platform compatibility (Claude + Gemini + OpenAI)

### Maximize Gemini Usage Score (30%)
- Use Gemini 3 Pro for ALL code generation
- Use Gemini for schema translation
- Use Gemini for code analysis/improvement
- Mention Gemini prominently in writeup and video

### Stand Out
- "Agents building tools for agents" is unique angle
- MCP integration for Claude Desktop is bonus
- Show the meta-use case: agent creating its own tools

---

## Quick Commands Reference

```bash
# Setup
cd gemini-competition/agentkit
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Run API
uvicorn src.api.main:app --reload

# Run CLI
agentkit generate "your tool description"

# Test
pytest tests/
```

---

## Files to Create

```
agentkit/
├── pyproject.toml            # Dependencies
├── .env                      # GEMINI_API_KEY
├── README.md                 # Project readme
├── writeup.md               ✅ Done
├── COMPETITION_ROADMAP.md   ✅ Done (this file)
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── generate.py   # POST /generate
│   │       └── tools.py      # GET /tools
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py           # Typer CLI
│   │
│   ├── generator/
│   │   ├── __init__.py
│   │   ├── backend_gen.py    # Generate FastAPI code
│   │   ├── schema_gen.py     # Generate agent schemas
│   │   └── mcp_gen.py        # Generate MCP server
│   │
│   └── core/
│       ├── __init__.py
│       ├── gemini.py         # Gemini client
│       └── schemas.py        # Pydantic models
│
├── generated/                # Output folder for generated tools
│
└── tests/
    └── test_generator.py
```

---

## Timeline Suggestion

| Day | Tasks |
|-----|-------|
| Day 1 (Today) | Setup + Core generator |
| Day 2 | API + CLI |
| Day 3 | Testing + Bug fixes |
| Day 4 | Demo video |
| Day 5 | Submit + Polish |

**Deadline: December 12, 2025**

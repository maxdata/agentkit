# AgentKit - Generate Backend Tools for AI Agents

## Category
**Technology**

## Summary
Describe what tool you need in natural language, get a complete backend with agent-ready function schemas for Claude, Gemini, and OpenAI - plus an MCP server for Claude Desktop integration.

## The Problem
AI agents need tools to be useful in the real world. But creating tools for agents requires:
- Writing the backend API from scratch
- Creating function schemas for each agent format (OpenAI, Claude, Gemini)
- Testing that agents can actually call the tools
- Maintaining multiple schema formats as APIs evolve

Developers spend more time on plumbing than on the actual tool logic. What if agents could build their own tools?

## The Solution
AgentKit uses Gemini 3 Pro to generate complete, agent-ready backends:

1. **Describe** the tool you need in natural language
2. **Generate** - Gemini creates the backend + all agent schemas automatically
3. **Deploy** - Get a ready-to-use tool that any AI agent can call
4. **Integrate** - Includes MCP server for instant Claude Desktop integration

### Example
**Input:** "A weather tool that gets current weather and forecasts for any city"

**Output:**
```
generated/weather-tool/
├── src/api/                    # FastAPI backend
├── agent_schemas/              # Claude, Gemini, OpenAI formats
├── mcp/                        # Claude Desktop MCP server
└── tests/
```

## How It Uses Gemini 3 Pro

AgentKit leverages Gemini 3 Pro's capabilities in three key ways:

### 1. Code Generation
Gemini generates the complete FastAPI backend with:
- Proper REST endpoints
- Pydantic models for validation
- Error handling
- Type hints throughout

### 2. Schema Translation
Gemini understands the nuances of each agent platform's function schema format:
- OpenAI function calling format
- Claude tool use format
- Gemini function declarations

This ensures generated tools work seamlessly across all major AI agent platforms.

### 3. Code Analysis & Improvement
Gemini analyzes generated code for:
- Security issues
- Performance optimizations
- Best practices
- Then auto-improves the code

## Demo Video
[Link to 2-minute demo video]

**Demo flow:**
1. Show AgentKit CLI generating a "bookmark manager" tool
2. Show generated files: FastAPI backend, agent schemas, MCP server
3. Start the server with `uvicorn`
4. Claude agent successfully calls the generated tool
5. "AgentKit - agents can build their own tools"

## Technical Architecture

```
agentkit/
├── src/
│   ├── api/              # AgentKit API
│   ├── cli/              # CLI interface
│   ├── generator/        # Tool generation engine
│   │   ├── planner.py    # Analyze requirements
│   │   ├── backend_gen.py
│   │   ├── schema_gen.py
│   │   └── mcp_gen.py
│   └── analyzer/         # Code analysis
└── generated/            # Output folder
```

**Stack:** Gemini Python SDK + Claude Agent SDK + FastAPI

## What Makes This Unique

1. **Agents building tools for agents** - A meta-level capability that unlocks autonomous agent workflows
2. **Multi-platform schemas** - One tool works with Claude, Gemini, and OpenAI
3. **MCP integration** - Instant Claude Desktop compatibility
4. **Practical output** - Real, working tools, not just demos

## Impact

AgentKit dramatically reduces the friction for building AI agent tools:
- **Before:** Hours/days to build a tool, write schemas, test integrations
- **After:** Minutes from description to working tool

This enables:
- Rapid prototyping of agent capabilities
- Non-developers creating tools via natural language
- Agents that can dynamically extend their own capabilities

## Links

- **GitHub:** [Link to repository]
- **Live Demo:** [Link if deployed]

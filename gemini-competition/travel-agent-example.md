# Gemini 3 Pro - Smart Travel Assist Agent

Reference implementation for building AI travel agents with Gemini.

## Architecture Overview

An agent has four essential components:

| Component | Description |
|-----------|-------------|
| **Model (Brain)** | Gemini reasoning engine for planning |
| **Tools (Hands)** | Functions that interact with external APIs |
| **Context/Memory** | Managed information accessible to agent |
| **Loop (Life)** | Iterative cycle: observe → think → act |

## Agent Loop Process

1. Define tools as JSON schemas (name, description, parameters)
2. Send user prompt + tool definitions to LLM
3. Model returns structured tool-use requests if needed
4. Execute tools client-side, capture results
5. Return results to model for next iteration

---

## Complete Implementation

### Step 1: Basic Agent Class

```python
from google import genai
from google.genai import types

class Agent:
    def __init__(self, model: str):
        self.model = model
        self.client = genai.Client()
        self.contents = []

    def run(self, contents: str):
        self.contents.append({"role": "user", "parts": [{"text": contents}]})
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.contents
        )
        self.contents.append(response.candidates[0].content)
        return response
```

### Step 2: Tool Definitions

```python
# Tool schema format
event_function = {
    "name": "event_api",
    "description": "Retrieves event information based on a query and optional filters.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The event search query (e.g., 'Events in Austin, TX')."
            },
            "htichips": {
                "type": "string",
                "description": """Date filter options:
                - 'date:today' - Today's events
                - 'date:tomorrow' - Tomorrow's events
                - 'date:week' - This week's events
                - 'date:weekend' - This weekend's events
                - 'date:next_week' - Next week's events
                - 'date:month' - This month's events"""
            }
        },
        "required": ["query"]
    }
}

hotel_function = {
    "name": "hotel_api",
    "description": "Retrieves hotel information based on location, dates, and preferences.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (location name)"
            },
            "check_in_date": {
                "type": "string",
                "description": "Check-in date in YYYY-MM-DD format"
            },
            "check_out_date": {
                "type": "string",
                "description": "Check-out date in YYYY-MM-DD format"
            },
            "hotel_class": {
                "type": "integer",
                "description": "Hotel rating: 2=2-star, 3=3-star, 4=4-star, 5=5-star"
            },
            "adults": {
                "type": "integer",
                "description": "Number of adults"
            }
        },
        "required": ["query", "check_in_date", "check_out_date"]
    }
}
```

### Step 3: API Implementations

```python
import requests
import os

SERP_API_KEY = os.environ.get("SERP_API_KEY", "your_key")

def event_api(query: str, htichips: str = "date:today"):
    """Fetch events from SerpAPI."""
    URL = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&engine=google_events&q={query}&htichips={htichips}&hl=en&gl=us"
    response = requests.get(URL).json()
    return response.get("events_results", [])

def hotel_api(
    query: str,
    check_in_date: str,
    check_out_date: str,
    hotel_class: int = 3,
    adults: int = 2
):
    """Fetch hotels from SerpAPI."""
    URL = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&engine=google_hotels&q={query}&check_in_date={check_in_date}&check_out_date={check_out_date}&adults={int(adults)}&hotel_class={int(hotel_class)}&currency=USD&gl=us&hl=en"
    response = requests.get(URL).json()
    return response.get("properties", [])
```

### Step 4: Agent with Tool Integration

```python
class TravelAgent:
    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.model = model
        self.client = genai.Client()
        self.contents = []
        self.tools = {
            "event_api": {"definition": event_function, "function": event_api},
            "hotel_api": {"definition": hotel_function, "function": hotel_api},
        }
        self.system_instruction = """You are a helpful Travel Assistant.
        Help users plan trips by finding events and hotels.
        Always be friendly and provide detailed recommendations."""

    def run(self, contents: str | list):
        if isinstance(contents, list):
            self.contents.append({"role": "user", "parts": contents})
        else:
            self.contents.append({"role": "user", "parts": [{"text": contents}]})

        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=[types.Tool(
                function_declarations=[
                    tool["definition"] for tool in self.tools.values()
                ]
            )],
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.contents,
            config=config
        )

        # IMPORTANT: Preserve thought signature for Gemini 3
        self.contents.append(response.candidates[0].content)

        # Handle function calls
        if response.function_calls:
            functions_response_parts = []
            for tool_call in response.function_calls:
                if tool_call.name in self.tools:
                    result = self.tools[tool_call.name]["function"](**tool_call.args)
                    result_data = {"result": result}
                else:
                    result_data = {"error": "Tool not found"}

                functions_response_parts.append({
                    "functionResponse": {
                        "name": tool_call.name,
                        "response": result_data
                    }
                })

            # Recursive call with function results
            return self.run(functions_response_parts)

        return response
```

### Step 5: CLI Interface

```python
from datetime import date

def mission_prompt(prompt: str):
    """Wrap user prompt with context."""
    today = date.today()
    return f"""Thought: Understand the request and determine if tools are needed.
Action:
- If APIs (event/hotel) are needed and I have required params, call them
- If more info needed, ask the user
- Otherwise, respond directly

[QUESTION] {prompt}
[TODAY] {today}"""

# Run the agent
agent = TravelAgent()
print("Travel Assistant ready. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = agent.run(mission_prompt(user_input))
    print(f"Agent: {response.text}\n")
```

---

## Example Queries

```python
# Find events
agent.run("What events are happening in Atlanta this weekend?")

# Find hotels
agent.run("Find me a 4-star hotel in Midtown Atlanta for Dec 20-22")

# Combined trip planning
agent.run("I want to visit San Francisco next week. Find events and hotels.")
```

---

## Best Practices for Travel Agents

### Tool Design
- **Clear naming**: `get_flights`, `search_hotels`, `find_events`
- **Precise descriptions**: Explain when/how to use each tool
- **Meaningful errors**: Enable agent self-correction
- **Fuzzy input tolerance**: Handle approximate dates/locations

### Context Engineering
- Don't dump entire datasets; use search functions
- Implement just-in-time loading via tool calls
- Compress history for long sessions
- Maintain persistent scratchpad for trip details

### System Design
- Add iteration limits (e.g., 15-turn max)
- Use system instructions for personality/guardrails
- Log all tool calls for debugging
- Human-in-the-loop for bookings

---

## Gemini 3 Specific Notes

### Thought Signatures
Gemini 3 generates encrypted "Thought Signatures" before tool calls. **You must return these exactly as received** in subsequent requests:

```python
# CORRECT: Preserve the full content including signature
self.contents.append(response.candidates[0].content)

# WRONG: Only saving text loses the signature
self.contents.append({"role": "model", "parts": [{"text": response.text}]})
```

### Thinking Level for Travel Queries

```python
# Simple queries (event list)
config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        thinking_level=types.ThinkingLevel.LOW
    )
)

# Complex planning (multi-city itinerary)
config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        thinking_level=types.ThinkingLevel.HIGH
    )
)
```

---

## Additional Tools to Add

| Tool | Purpose | API |
|------|---------|-----|
| `flight_search` | Find flights | Google Flights via SerpAPI |
| `restaurant_search` | Find restaurants | Google Places API |
| `weather_forecast` | Get weather | OpenWeatherMap |
| `attraction_search` | Find attractions | Google Places API |
| `currency_convert` | Convert currencies | Exchange Rate API |

---

## Sources

- [Practical Guide: Building Agents with Gemini 3](https://www.philschmid.de/building-agents)
- [Google Cloud: Trip Planning Agent Tutorial](https://cloud.google.com/blog/topics/developers-practitioners/learn-how-to-create-an-ai-agent-for-trip-planning-with-gemini-1-5-pro)
- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Kaggle Competition](https://www.kaggle.com/competitions/gemini-3/)

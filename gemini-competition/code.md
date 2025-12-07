# Gemini 3 Pro API - Code Examples & Documentation

Compiled: December 7, 2025

## Model Specifications

| Spec | Value |
|------|-------|
| **Model ID** | `gemini-3-pro-preview` |
| **Max Input Tokens** | 1,048,576 (1M) |
| **Max Output Tokens** | 65,536 (64K) |
| **Knowledge Cutoff** | January 2025 |
| **Pricing** | $2/$12 per million tokens (input/output) |
| **Launch** | November 18, 2025 (public preview) |

### Supported I/O

| Input | Output |
|-------|--------|
| Text, Code, Images, Audio, Video, PDF | Text only |

---

## Installation & Setup

```bash
# Install SDK (requires v1.51.0+)
pip install --upgrade google-genai

# Environment variables
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True
```

---

## Basic Usage

### Simple Text Generation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="How does AI work?",
)
print(response.text)
```

### With Thinking Level Control

**LOW** - Fast responses, minimal reasoning:
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="How does AI work?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.LOW
        )
    ),
)
```

**HIGH** - Complex reasoning tasks:
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Solve this multi-step problem...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.HIGH
        )
    ),
)
```

---

## Multimodal Input

### Image Analysis with Media Resolution

Per-part resolution:
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[
        types.Part(
            file_data=types.FileData(
                file_uri="gs://bucket/image.jpg",
                mime_type="image/jpeg",
            ),
            media_resolution=types.PartMediaResolution(
                level=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH
            ),
        ),
        "What is in the image?",
    ],
)
```

Global resolution:
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[contents],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
    ),
)
```

### Media Resolution Token Costs

| Resolution | Images | Video/frame | PDFs |
|------------|--------|-------------|------|
| LOW | 280 | 70 | 280 |
| MEDIUM | 560 | 70 | 560 |
| HIGH | 1120 | 280 | 1120 |

---

## Function Calling

### Manual Two-Turn with Thought Signatures

```python
# Define tool
get_weather_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Gets current weather temperature.",
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
)
tool_config = types.Tool(function_declarations=[get_weather_declaration])

# Initial request
response_1 = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="What's the weather in London?",
    config=types.GenerateContentConfig(tools=[tool_config]),
)

# Process function call
function_call = response_1.function_calls[0]
location = function_call.args["location"]

# Execute tool (mock)
function_response_data = {"location": location, "temperature": "30C"}

# Send result back - PRESERVE THOUGHT SIGNATURE
history = [
    types.Content(role="user", parts=[types.Part(text="What's the weather in London?")]),
    response_1.candidates[0].content,  # Contains thought signature
    types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response=function_response_data,
            )
        ],
    )
]

response_2 = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=history,
    config=types.GenerateContentConfig(tools=[tool_config]),
)
print(f"Final response: {response_2.text}")
```

### Automatic Function Calling

```python
def get_current_temperature(location: str) -> dict:
    """Gets current temperature for a location."""
    return {"temperature": 25, "unit": "Celsius"}

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="What's the temperature in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_temperature],
    )
)
print(response.text)
```

### Streaming Function Calls

```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-pro-preview",
    contents="What's the weather in London and New York?",
    config=types.GenerateContentConfig(
        tools=[get_weather_tool],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=types.FunctionCallingConfigMode.AUTO,
                stream_function_call_arguments=True,
            )
        ),
    ),
):
    function_call = chunk.function_calls[0]
    if function_call and function_call.name:
        print(f"{function_call.name}")
```

### Multimodal Function Responses

```python
get_image_declaration = types.FunctionDeclaration(
    name="get_image",
    description="Retrieves image for order items.",
    parameters={
        "type": "object",
        "properties": {"item_name": {"type": "string"}},
        "required": ["item_name"],
    },
)

response_1 = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=["Show me the green shirt I ordered."],
    config=types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=[get_image_declaration])],
    )
)

# Return image in function response
function_response_multimodal = types.FunctionResponsePart(
    file_data=types.FunctionResponseFileData(
        mime_type="image/png",
        display_name="dress.jpg",
        file_uri="gs://bucket/dress.jpg",
    )
)

history = [
    types.Content(role="user", parts=[types.Part(text="Show me the green shirt...")]),
    response_1.candidates[0].content,
    types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name="get_image",
                response={"image_ref": {"$ref": "dress.jpg"}},
                parts=[function_response_multimodal]
            )
        ],
    )
]

response_2 = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=history,
    config=types.GenerateContentConfig(tools=[tool_config]),
)
```

---

## OpenAI Compatibility Layer

```python
import openai
from google.auth import default

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

client = openai.OpenAI(
    base_url=f"https://aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/global/endpoints/openapi",
    api_key=credentials.token,
)

response = client.chat.completions.create(
    model="gemini-3-pro-preview",
    reasoning_effort="medium",
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

---

## Key Parameters Reference

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `thinking_level` | LOW, HIGH | HIGH | Replaces `thinking_budget` |
| `temperature` | 0.0-2.0 | 1.0 | **Keep at 1.0** - lower causes looping |
| `topP` | 0.0-1.0 | 0.95 | Nucleus sampling |
| `topK` | - | 64 | Fixed value |
| `candidateCount` | 1-8 | 1 | Number of responses |
| `media_resolution` | LOW, MEDIUM, HIGH | varies | Control token usage |

---

## Media Limits

| Modality | Limit |
|----------|-------|
| **Images** | Max 900/prompt, 7MB console / 30MB Cloud Storage |
| **PDFs** | Max 900 files, 900 pages each, 50MB API |
| **Video** | ~45 min with audio, ~1 hour without, max 10/prompt |
| **Audio** | ~8.4 hours max, 1 file per prompt |

---

## Supported Features

| Feature | Status |
|---------|--------|
| Google Search grounding | ✅ |
| Code execution | ✅ |
| System instructions | ✅ |
| Structured output | ✅ |
| Function calling (streaming) | ✅ |
| Token counting | ✅ |
| Thinking mode | ✅ |
| Context caching | ✅ |
| RAG Engine | ✅ |
| Chat completions | ✅ |
| Image output | ❌ |
| Tuning | ❌ |
| Gemini Live API | ❌ |

---

## Kaggle Notebooks

| Notebook | Link |
|----------|------|
| Gemini 3 Pro Starter | [kaggle.com/code/prathameshbang/gemini-3-pro-starter-notebook](https://www.kaggle.com/code/prathameshbang/gemini-3-pro-starter-notebook) |
| Gemini 3 Pro API Model | [kaggle.com/models/google/gemini-3-pro-api](https://www.kaggle.com/models/google/gemini-3-pro-api) |
| Gemini API Starter | [kaggle.com/code/prathameshbang/gemini-api-starter-notebook](https://www.kaggle.com/code/prathameshbang/gemini-api-starter-notebook) |

---

## Sources

- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Vertex AI Gemini 3 Pro Docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro)
- [Get Started with Gemini 3](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/get-started-with-gemini-3)
- [Kaggle Competition](https://www.kaggle.com/competitions/gemini-3/)

#!/bin/bash
# AgentKit Demo Script
# Run this while screen recording (Cmd+Shift+5 on Mac)

cd /Users/max/Documents/GitHub/agentkit
source .venv/bin/activate

clear
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  AgentKit - Generate Backend Tools for AI Agents"
echo "  Powered by Gemini 3 Pro"
echo "═══════════════════════════════════════════════════════════════"
echo ""
sleep 3

echo "📝 Let's generate a bookmark manager tool..."
echo ""
sleep 2

echo "$ agentkit generate \"A bookmark manager with add, search, and tag operations\""
echo ""
sleep 2

# Run the actual generation
agentkit generate "A bookmark manager with add, search, and tag operations"

sleep 3
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  ✅ Tool generated! Let's look at the Claude schema..."
echo "═══════════════════════════════════════════════════════════════"
echo ""
sleep 2

# Find the most recent generated folder
LATEST=$(ls -td generated/*/ | head -1)
echo "$ cat ${LATEST}agent_schemas/claude_tools.json"
echo ""
sleep 1
cat ${LATEST}agent_schemas/claude_tools.json | head -40
echo ""
sleep 4

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🚀 AgentKit - Agents can build their own tools!"
echo "  GitHub: https://github.com/maxdata/agentkit"
echo "═══════════════════════════════════════════════════════════════"
echo ""
sleep 3

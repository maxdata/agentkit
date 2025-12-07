# AgentKit Demo Video
# Run with: vhs demo.tape

Output demo.mp4
Output demo.gif

Set FontSize 18
Set Width 1200
Set Height 800
Set Theme "Catppuccin Mocha"
Set Padding 20

Type "# AgentKit - Generate Backend Tools for AI Agents"
Enter
Sleep 2s

Type "# Powered by Gemini 3 Pro"
Enter
Sleep 2s

Type "cd /Users/max/Documents/GitHub/agentkit && source .venv/bin/activate"
Enter
Sleep 1s

Type "# Let's generate a bookmark manager tool..."
Enter
Sleep 2s

Type@50ms "agentkit generate 'A bookmark manager with add, search, and tag operations'"
Enter
Sleep 15s

Type "# Tool generated! Let's see the Claude schema:"
Enter
Sleep 2s

Type "cat generated/*/agent_schemas/claude_tools.json | head -30"
Enter
Sleep 5s

Type "# AgentKit - Agents can build their own tools!"
Enter
Sleep 3s

Type "# GitHub: https://github.com/maxdata/agentkit"
Enter
Sleep 3s

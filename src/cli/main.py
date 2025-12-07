"""CLI interface for AgentKit."""

import asyncio
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import json

from src.generator import generate_tool, list_projects, get_project, get_schema

app = typer.Typer(
    name="agentkit",
    help="Generate backend tools for AI agents with Gemini 3 Pro",
)
console = Console()


@app.command()
def generate(
    description: str = typer.Argument(..., help="Natural language description of the tool"),
    name: str = typer.Option(None, "--name", "-n", help="Tool name (auto-generated if not provided)"),
    requirements: list[str] = typer.Option([], "--req", "-r", help="Additional requirements"),
    output: str = typer.Option("generated", "--output", "-o", help="Output directory"),
):
    """Generate a new agent tool from a description."""
    console.print(Panel(
        f"[bold blue]AgentKit[/bold blue] - Generating tool from description",
        subtitle="Powered by Gemini 3 Pro"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing requirements...", total=None)

        async def run():
            progress.update(task, description="Generating code with Gemini 3 Pro...")
            project_id, tool = await generate_tool(
                description=description,
                name=name,
                requirements=requirements,
                output_dir=output,
            )
            return project_id, tool

        project_id, tool = asyncio.run(run())

    # Display results
    console.print()
    console.print(f"[green]Tool generated successfully![/green]")
    console.print()

    table = Table(title="Generated Tool")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Project ID", project_id)
    table.add_row("Name", tool.name)
    table.add_row("Description", tool.description)
    table.add_row("Functions", str(len(tool.tools)))
    table.add_row("Files", str(len(tool.files)))
    console.print(table)

    console.print()
    console.print("[bold]Generated files:[/bold]")
    for f in tool.files:
        console.print(f"  [dim]{f.path}[/dim]")

    console.print()
    console.print("[bold]Functions:[/bold]")
    for func in tool.tools:
        console.print(f"  [cyan]{func['name']}[/cyan] - {func['description']}")

    console.print()
    console.print(f"[dim]Run the tool: cd {output}/{tool.name}-{project_id} && uvicorn src.api.main:app[/dim]")


@app.command()
def list():
    """List all generated tools."""
    projects = list_projects()

    if not projects:
        console.print("[yellow]No tools generated yet.[/yellow]")
        console.print("Run: agentkit generate \"your tool description\"")
        return

    table = Table(title="Generated Tools")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Description", style="dim")
    table.add_column("Created", style="green")

    for p in projects:
        table.add_row(
            p["project_id"],
            p["name"],
            p["description"][:50] + "..." if len(p["description"]) > 50 else p["description"],
            p["created_at"][:19],
        )

    console.print(table)


@app.command()
def schema(
    project_id: str = typer.Argument(..., help="Project ID"),
    format: str = typer.Option("combined", "--format", "-f", help="Schema format: openai, claude, gemini, combined"),
):
    """Get agent schema for a generated tool."""
    result = get_schema(project_id, format)

    if not result:
        console.print(f"[red]Project not found: {project_id}[/red]")
        raise typer.Exit(1)

    console.print(Panel(f"[bold]Schema ({format})[/bold]"))
    console.print(Syntax(json.dumps(result, indent=2), "json", theme="monokai"))


@app.command()
def info(project_id: str = typer.Argument(..., help="Project ID")):
    """Get details of a generated tool."""
    project = get_project(project_id)

    if not project:
        console.print(f"[red]Project not found: {project_id}[/red]")
        raise typer.Exit(1)

    tool = project["tool"]

    console.print(Panel(f"[bold]{tool.name}[/bold]"))

    table = Table()
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Project ID", project_id)
    table.add_row("Name", tool.name)
    table.add_row("Description", tool.description)
    table.add_row("Path", project["path"])
    table.add_row("Created", project["created_at"])
    console.print(table)

    console.print()
    console.print("[bold]Functions:[/bold]")
    for func in tool.tools:
        console.print(f"  [cyan]{func['name']}[/cyan]")
        console.print(f"    {func['description']}")
        if func.get("parameters", {}).get("properties"):
            for param, details in func["parameters"]["properties"].items():
                required = param in func["parameters"].get("required", [])
                req_str = "[red]*[/red]" if required else ""
                console.print(f"    - {param}{req_str}: {details.get('type', 'any')}")


if __name__ == "__main__":
    app()

"""Interactive Command Line Interface (CLI) for Autonomous Codebase Knowledge Graph Navigator."""

import argparse
import os
import sys
from typing import Optional

# Ensure Task 2 directory is in sys.path for direct script execution
task_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if task_root not in sys.path:
    sys.path.insert(0, task_root)

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from src.agent.navigator import AutonomousCodebaseNavigator
from src.graph.mock_graph_client import MockGraphClient
from src.mcp.tools import GraphToolRegistry

console = Console()


def print_banner() -> None:
    """Display terminal banner."""
    banner_text = (
        "[bold cyan]Autonomous Codebase Knowledge Graph Navigator[/bold cyan]\n"
        "[dim]G41 - AI/ML | Enterprise Architecture Blast-Radius & Refactoring Agent[/dim]"
    )
    console.print(Panel(banner_text, border_style="cyan"))


def display_schema(client: MockGraphClient) -> None:
    """Render graph schema in formatted rich tables."""
    schema = client.get_schema()

    console.print(f"\n[bold green]Knowledge Graph Summary:[/bold green] {schema['total_nodes']} nodes, {schema['total_edges']} relationships")

    table = Table(title="Node Categories & Counts", header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")

    for cat, count in schema["node_type_counts"].items():
        table.add_row(cat, str(count))
    console.print(table)

    rel_table = Table(title="Relationship Types & Counts", header_style="bold magenta")
    rel_table.add_column("Relationship Type", style="yellow")
    rel_table.add_column("Count", justify="right", style="green")

    for rel, count in schema["relationship_type_counts"].items():
        rel_table.add_row(f"[:{rel}]", str(count))
    console.print(rel_table)


def display_cycles(client: MockGraphClient) -> None:
    """Render detected circular dependencies."""
    cycles = client.detect_cycles()
    if not cycles:
        console.print("[green]No circular dependencies detected. Graph is clean DAG.[/green]")
        return

    console.print(f"[bold red]Warning:[/bold red] Found {len(cycles)} circular dependency loops:")
    for idx, cycle in enumerate(cycles, 1):
        chain = " -> ".join([f"[bold yellow]{node}[/bold yellow]" for node in cycle])
        console.print(f"  {idx}. {chain} -> [bold yellow]{cycle[0]}[/bold yellow]")


def display_blast_radius(client: MockGraphClient, node_id: str) -> None:
    """Render blast-radius analysis table for a component."""
    try:
        br = client.calculate_blast_radius(node_id)
    except KeyError:
        console.print(f"[bold red]Error:[/bold red] Component '{node_id}' not found in graph.")
        return

    console.print(Panel(
        f"[bold]Target Component:[/bold] {br['target_name']} ({br['target_type']})\n"
        f"[bold]Total Downstream Affected Components:[/bold] [bold red]{br['total_affected_count']}[/bold red] (Source excluded)\n"
        f"[bold]Direct Dependents:[/bold] {len(br['direct_dependents'])}\n"
        f"[bold]Indirect Dependents:[/bold] {len(br['indirect_dependents'])}",
        title=f"Blast Radius Analysis: {node_id}",
        border_style="red",
    ))

    table = Table(title="Affected Components by Category", header_style="bold cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Affected Count", justify="right", style="yellow")
    table.add_column("Components", style="white")

    for cat, items in br["affected_by_category"].items():
        table.add_row(cat, str(len(items)), ", ".join(items))
    console.print(table)


def run_query(navigator: AutonomousCodebaseNavigator, query: str) -> None:
    """Run natural language query through navigator and render Markdown report."""
    console.print(f"\n[dim]Analyzing inquiry:[/dim] [bold white]\"{query}\"[/bold white]...")
    result = navigator.navigate(query)

    console.print("\n[dim]Intent Detected:[/dim] [cyan]{}[/cyan]".format(result.parsed_intent.intent.value))
    if result.cypher_result.is_valid:
        console.print("[dim]Generated Cypher (Read-Only):[/dim]")
        console.print(Panel(result.cypher_result.cypher_query, style="dim green"))

    console.print(Panel(Markdown(result.report_markdown), title="Technical Architecture Report", border_style="cyan"))


def interactive_repl(navigator: AutonomousCodebaseNavigator, client: MockGraphClient) -> None:
    """Run interactive terminal REPL."""
    print_banner()
    console.print("[dim]Type your architecture question, or 'schema', 'cycles', 'help', 'exit'.[/dim]\n")

    while True:
        try:
            query = console.input("[bold cyan]navigator>[/bold cyan] ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                console.print("[dim]Goodbye![/dim]")
                break
            elif query.lower() in ("schema", "info"):
                display_schema(client)
            elif query.lower() == "cycles":
                display_cycles(client)
            elif query.lower() == "help":
                console.print(
                    "Sample questions you can ask:\n"
                    "  - If I deprecate the legacy authentication module, which downstream API routes and frontend components will break?\n"
                    "  - What does order-service depend on?\n"
                    "  - What is the blast radius of order-service?\n"
                    "  - Analyze coupling of payment-service\n"
                    "  - Find circular dependencies\n"
                    "  - Search for database nodes\n"
                    "Commands: schema, cycles, exit"
                )
            else:
                run_query(navigator, query)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Exiting...[/dim]")
            break


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Autonomous Codebase Knowledge Graph Navigator CLI")
    parser.add_argument("-q", "--query", type=str, help="Natural language architecture inquiry")
    parser.add_argument("-b", "--blast-radius", type=str, help="Analyze blast radius of a specific component ID")
    parser.add_argument("-s", "--schema", action="store_true", help="Display graph schema and counts")
    parser.add_argument("-c", "--cycles", action="store_true", help="Display circular dependencies")

    args = parser.parse_args()

    client = MockGraphClient()
    registry = GraphToolRegistry(graph_client=client)
    navigator = AutonomousCodebaseNavigator(graph_client=client, tool_registry=registry)

    if args.schema:
        print_banner()
        display_schema(client)
    elif args.cycles:
        print_banner()
        display_cycles(client)
    elif args.blast_radius:
        print_banner()
        display_blast_radius(client, args.blast_radius)
    elif args.query:
        print_banner()
        run_query(navigator, args.query)
    else:
        interactive_repl(navigator, client)


if __name__ == "__main__":
    main()


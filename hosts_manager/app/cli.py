import typer
from typing import List
from hosts_manager.app.core import (
    detect_hosts_path,
    parse_hosts,
    add_entry,
    toggle_entry,
    remove_entry,
    backup_hosts,
)

app = typer.Typer(help="hostctl: Manage your system hosts file easily.")

def get_hosts_path() -> str:
    """Detects hosts file path and returns it."""
    try:
        return detect_hosts_path()
    except FileNotFoundError:
        typer.echo("❌ Hosts file not found on this system.")
        raise typer.Exit(code=1)

@app.command(help="List all host entries with their status.")
def list():
    path = get_hosts_path()
    entries = parse_hosts(path)
    if not entries:
        typer.echo("No host entries found.")
        return

    for idx, e in enumerate(entries):
        status = "ENABLED" if e.enabled else "DISABLED"
        hosts = " ".join(e.hostnames)
        comment = f"#{e.comment}" if e.comment else ""
        typer.echo(f"[{idx}] {status:8} {e.ip:<15} {hosts:<30} {comment}")

@app.command(help="Add a new host entry.")
def add(ip: str, hostnames: List[str], comment: str = typer.Option("", help="Optional comment")):
    path = get_hosts_path()
    add_entry(path, ip, hostnames, comment)
    typer.echo(f"✅ Added {ip} -> {' '.join(hostnames)}")

@app.command(help="Enable a host entry by hostname.")
def enable(hostname: str):
    path = get_hosts_path()
    toggle_entry(path, hostname, True)
    typer.echo(f"✅ Enabled entry for {hostname}")

@app.command(help="Disable a host entry by hostname.")
def disable(hostname: str):
    path = get_hosts_path()
    toggle_entry(path, hostname, False)
    typer.echo(f"✅ Disabled entry for {hostname}")

@app.command(help="Remove a host entry by hostname.")
def remove(hostname: str):
    path = get_hosts_path()
    remove_entry(path, hostname)
    typer.echo(f"✅ Removed entry for {hostname}")

@app.command(help="Backup the hosts file.")
def backup(destination: str = typer.Option("", help="Optional backup path")):
    path = get_hosts_path()
    backup_file = backup_hosts(path)
    typer.echo(f"✅ Backup created: {backup_file}")

if __name__ == "__main__":
    app()

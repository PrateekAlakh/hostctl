import os
import re
import shutil
import datetime
from typing import List, Optional

from hosts_manager.app.utils import is_ip

# Common paths
HOSTS_PATHS = [
    "/etc/hosts",  # Linux/Mac
    r"C:\Windows\System32\drivers\etc\hosts",  # Windows
]

class HostsEntry:
    def __init__(self, ip: str, hostnames: List[str], comment: str = "", enabled: bool = True, raw: str = ""):
        self.ip = ip
        self.hostnames = hostnames
        self.comment = comment
        self.enabled = enabled
        self.raw = raw  # Original line, for preservation

    def __repr__(self):
        status = "ENABLED" if self.enabled else "DISABLED"
        return f"<{status} {self.ip} {self.hostnames} #{self.comment}>"

def detect_hosts_path() -> str:
    for p in HOSTS_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("No hosts file found on this system.")

def backup_hosts(path: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{path}.backup.{timestamp}"
    shutil.copy(path, backup_file)
    return backup_file

def parse_hosts(path: str) -> List[HostsEntry]:
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.rstrip("\n")
            if not raw.strip():
                continue  # skip blank lines
            enabled = not raw.strip().startswith("#")
            line_content = raw.lstrip("#").strip()
            match = re.match(r"^(\S+)\s+(.+?)(?:\s+#\s*(.*))?$", line_content)
            if match and is_ip(match.group(1)):
                ip = match.group(1)
                hostnames = match.group(2).split()
                comment = match.group(3) or ""
                entries.append(HostsEntry(ip, hostnames, comment, enabled, raw))

    return entries

def write_hosts(path: str, entries: List[HostsEntry]) -> None:
    lines = []
    for e in entries:
        line = f"{e.ip}\t{' '.join(e.hostnames)}"
        if e.comment:
            line += f" # {e.comment}"
        if not e.enabled:
            line = "# " + line
        lines.append(line)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def add_entry(path: str, ip: str, hostnames: List[str], comment: str = "") -> None:
    entries = parse_hosts(path)
    entries.append(HostsEntry(ip, hostnames, comment, enabled=True))
    backup_hosts(path)
    write_hosts(path, entries)

def toggle_entry(path: str, target: str, enable: bool) -> None:
    entries = parse_hosts(path)
    backup_hosts(path)
    for e in entries:
        if target in e.hostnames:
            e.enabled = enable
    write_hosts(path, entries)

def remove_entry(path: str, target: str) -> None:
    entries = parse_hosts(path)
    backup_hosts(path)
    entries = [e for e in entries if target not in e.hostnames]
    write_hosts(path, entries)

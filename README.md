# hostctl – Hosts File Manager CLI

## Introduction
`hostctl` is a simple Python CLI tool to **view, add, remove, enable, or disable entries in your system's hosts file**. Works on macOS, Linux, and Windows.

---

## Features

- List all host entries (enabled/disabled)
- Add a new host entry with optional comment
- Enable or disable existing host entries
- Remove a host entry
- Backup your hosts file safely
- Works with IPv4 and IPv6 entries

[//]: # (---)

[//]: # ()
[//]: # (## Directory Structure)

[//]: # ()
[//]: # (```)

[//]: # (hosts_manager/)

[//]: # (├── app/)

[//]: # (│ ├── init.py)

[//]: # (│ ├── cli.py)

[//]: # (│ ├── core.py)

[//]: # (│ └── utils.py)

[//]: # (├── pyproject.toml)

[//]: # (├── README.md)

[//]: # (```)

---

## Prerequisites

- Python >= 3.9
- pip
- Virtual environment (recommended)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hosts_manager.git
cd hosts_manager
```
2. Create a virtual environment and activate it:
```
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```
3. Install the package in editable mode:
```
pip install -e .
```
## Usage
### Check help
```
hostctl --help
```
### List entries
```
hostctl list
```
### Add a host entry
```
sudo hostctl add 127.0.0.1 mysite.local --comment "local dev"
```
### Enable or disable an entry
```
sudo hostctl enable mysite.local
sudo hostctl disable mysite.local
```
### Remove an entry
```
sudo hostctl remove mysite.local
```
### Backup hosts file
```
hostctl backup
```
---
## Notes
- On macOS/Linux, modifying /etc/hosts requires root permissions. Use sudo for add/remove/enable/disable commands.

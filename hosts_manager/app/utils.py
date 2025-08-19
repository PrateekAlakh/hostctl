import shutil
import ipaddress

def is_ip(addr: str) -> bool:
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

def restore_hosts(path: str, backup_file: str) -> None:
    shutil.copy(backup_file, path)

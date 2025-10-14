from typing import List, Tuple, Optional

def parse_command(line: str) -> Optional[Tuple[str, List[str]]]:
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    parts = s.split()
    cmd = parts[0].upper()
    args = parts[1:]
    return cmd, args

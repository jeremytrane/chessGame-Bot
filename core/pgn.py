import re

def load_pgn(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        content = f.read()

    # Remove PGN headers
    content = '\n'.join(line for line in content.splitlines() if not line.startswith('['))

    # Remove game result
    content = re.sub(r"(1-0|0-1|1/2-1/2|\*)", "", content)

    tokens = content.strip().split()
    return [t for t in tokens if not t.endswith('.')]

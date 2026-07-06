# Python Snippets

## Pathlib (rutas modernas)
```python
from pathlib import Path

BASE = Path(__file__).parent
cfg = BASE / "config" / "settings.json"
cfg.write_text('{}')
data = cfg.read_text()
for p in BASE.rglob("*.py"):
    print(p.name)
```

## Async / Await
```python
import asyncio
from httpx import AsyncClient

async def fetch(url: str) -> dict:
    async with AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def main():
    results = await asyncio.gather(
        fetch("https://api.example.com/a"),
        fetch("https://api.example.com/b"),
    )
```

## Argparse
```python
import argparse

parser = argparse.ArgumentParser(description="Tool description")
parser.add_argument("-n", "--name", required=True, help="Nombre")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()
```

## Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)
```

## Manejo de archivos (shutil)
```python
import shutil

shutil.copy2(src, dst)        # preserva metadatos
shutil.copytree(src, dst)     # recursivo
shutil.rmtree(path)           # elimina directorio completo
shutil.make_archive("backup", "zip", "dir/")
```

## subprocess moderno
```python
import subprocess

r = subprocess.run(["git", "status"], capture_output=True, text=True)
print(r.stdout)
if r.returncode != 0:
    print("Error:", r.stderr)
```

"""Load ~/.env into os.environ. Overrides existing vars (broken user-scope wins lose)."""
import os


def load(path: str = "~/.env") -> None:
    p = os.path.expanduser(path)
    if not os.path.exists(p):
        return
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            if k.startswith("export "):
                k = k[len("export "):].strip()
            v = v.strip().strip('"').strip("'")
            if k:
                os.environ[k] = v

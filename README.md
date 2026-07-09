# A2DDoS — by Ayush Rajdev

**2 files. No bloat.**

## Files

| File | What |
|------|------|
| `A2DDoS.py` | Python version — needs Python |
| `A2DDoS.bat` | Launcher — double-click or run in cmd |

Both do the same thing.

## Usage

```bash
A2DDoS <target> <mode>
A2DDoS.bat <target> <mode>
```

**Target:** IP or URL (auto-adds http:// if missing)

**Modes:**
- `http` — HTTP flood (default)
- `slowloris` — Connection exhaustion
- `syn` — Rapid TCP connections
- `dns` — UDP query flood

**Options:**
- `--t 50` — Thread count
- `--c 500` — Max conns (slowloris)

## Examples

```bash
A2DDoS 192.168.1.100           # HTTP flood an IP
A2DDoS.bat localhost:8080      # Test your Docker
A2DDoS example.com slowloris   # Slowloris attack
A2DDoS 10.0.0.5 syn --t 100   # SYN sim, 100 threads
```

## Docker Lab (learn safely)

```bash
docker compose up -d                  # Start target
A2DDoS.bat localhost:8080             # Attack it
bash defense/rate_limit.sh            # Block it
```

## License

MIT — learn, experiment, defend.

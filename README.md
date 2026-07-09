# A2DDoS — by Ayush Rajdev

## Files

| File | Size | Needs Python? |
|------|------|--------------|
| `A2DDoS.exe` | ~8MB | **No** — standalone |
| `A2DDoS.py` | 3KB | Yes |
| `A2DDoS.bat` | 200B | Auto-detects: uses .exe first, .py if no exe |

**Just download `A2DDoS.exe` and you're done.**

## Usage (any of these work)

```
A2DDoS.exe 192.168.1.100
A2DDoS.bat 192.168.1.100
python A2DDoS.py 192.168.1.100
```

### Modes
```
A2DDoS <target> <mode>

Modes: http (default), slowloris, syn, dns
Options: --t <threads>  --c <max_conns>
```

## Examples

| Command | What it does |
|---------|-------------|
| `A2DDoS 192.168.1.100` | HTTP flood an IP |
| `A2DDoS localhost:8080` | Test your Docker |
| `A2DDoS example.com slowloris` | Connection exhaustion |
| `A2DDoS 10.0.0.5 syn --t 100` | SYN sim, 100 threads |
| `A2DDoS example.com dns` | DNS query flood |

## Docker Lab (learn safely)

```bash
docker compose up -d
A2DDoS localhost:8080         # Attack your own server
bash defense/rate_limit.sh    # Block it — watch it recover
```

## License

MIT — learn, experiment, defend.

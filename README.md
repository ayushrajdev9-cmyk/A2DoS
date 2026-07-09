# A2DoS — Safe DoS Testing Lab

**Made by Ayush Rajdev**

Learn DoS/DDoS concepts safely inside your own Docker environment. Attack only your own containers — zero legal risk, maximum learning.

## Features

```
A2DoS/
├── attacks.py            # 4 attack modes: http, slowloris, syn, dns
├── dashboard.py          # Live monitoring TUI (RPS, response time, status)
├── auto_demo.py          # One-command full lifecycle demo
├── plot_stats.py         # Graph attack stats from CSV (requires matplotlib)
├── docker-compose.yml    # Vulnerable Nginx target
├── nginx/
│   ├── conf.d/default.conf      # Unprotected
│   ├── conf.d/defense.conf      # Nginx limits (comment in)
│   └── html/index.html
├── defense/
│   ├── rate_limit.sh            # iptables rate limiting (Linux)
│   ├── limit_connections.sh     # iptables connlimit (Linux)
│   ├── defend.ps1               # Windows firewall defense (PowerShell)
│   └── monitor.sh               # Watch connections live
├── lab.py                # HTTP flood (legacy)
├── slowloris.py          # Slowloris (legacy)
├── requirements.txt
└── README.md
```

## Quick start

```bash
docker compose up -d
pip install -r requirements.txt
```

### Attack modes

| Mode | Command | What it does |
|------|---------|-------------|
| HTTP flood | `python attacks.py http://localhost:8080 http` | 50 threads of GET requests |
| Slowloris | `python attacks.py http://localhost:8080 slowloris` | Hold 500 connections open |
| SYN sim | `python attacks.py http://localhost:8080 syn` | Rapid TCP connections |
| DNS sim | `python attacks.py http://localhost:8080 dns` | Rapid UDP queries |

### Save & plot stats

```bash
python attacks.py http://localhost:8080 http --csv attack_log.csv
python plot_stats.py attack_log.csv
```

### Live dashboard

```bash
python dashboard.py http://localhost:8080
```

### Auto demo (attack → defense → recovery)

```bash
python auto_demo.py http://localhost:8080
```

### Defense

| Platform | HTTP flood | Slowloris | Revert |
|----------|-----------|-----------|--------|
| Linux | `bash defense/rate_limit.sh` | `bash defense/limit_connections.sh` | `bash defense/rate_limit.sh revert` |
| Windows | `.\defense\defend.ps1 -Action rate` | `.\defense\defend.ps1 -Action conn` | `.\defense\defend.ps1 -Action revert` |
| Nginx | Uncomment `nginx/conf.d/defense.conf` | Same | Comment out |

## License

MIT — learn, experiment, defend.

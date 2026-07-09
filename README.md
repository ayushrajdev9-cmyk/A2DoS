# DDoSLab — Safe DoS Testing Lab

**Made by Ayush Rajdev**

Learn DoS/DDoS concepts safely inside your own Docker environment.
Attack only your own containers — zero legal risk, maximum learning.

## What's inside

```
DDoSLab/
├── lab.py               # Educational HTTP flood tool (attack your lab only)
├── docker-compose.yml   # Spins up a vulnerable target server
├── nginx/
│   ├── conf.d/default.conf   # Target config (no rate limits initially)
│   └── html/index.html       # Target page
├── defense/
│   ├── rate_limit.sh         # Apply iptables rate limiting
│   └── monitor.sh            # Watch connections in real-time
└── requirements.txt
```

## Quick start

```bash
# 1. Start the target server
docker compose up -d

# 2. Install Python deps
pip install -r requirements.txt

# 3. Attack your own server
python lab.py http://localhost:8080

# 4. Watch it struggle
http://localhost:8080

# 5. Apply defense
bash defense/rate_limit.sh
```

## What you'll learn

- How HTTP floods work (threaded GET requests)
- How rate limiting mitigates them
- How to monitor connections with `netstat` / `ss`
- How fail2ban-style blocking works

## One-click defense demo

```bash
# terminal 1: start the attack
python lab.py http://localhost:8080

# terminal 2: see the flood in real-time (run while attacking)
bash defense/monitor.sh

# terminal 3: apply rate limiting (run while attacking)
bash defense/rate_limit.sh
# Watch the attack fail immediately
# Revert with: bash defense/rate_limit.sh revert
```

## License

MIT — learn, experiment, defend.

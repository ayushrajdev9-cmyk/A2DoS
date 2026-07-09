# A2DoS — Safe DoS Testing Lab

**Made by Ayush Rajdev**

Learn DoS/DDoS concepts safely inside your own Docker environment.
Attack only your own containers — zero legal risk, maximum learning.

## What's inside

```
A2DoS/
├── lab.py               # HTTP flood attack (RPS display)
├── slowloris.py         # Connection exhaustion attack (slowloris)
├── docker-compose.yml   # Spins up a vulnerable Nginx target
├── nginx/
│   ├── conf.d/
│   │   ├── default.conf      # Unprotected target
│   │   └── defense.conf      # Nginx rate/conn limits (comment in to enable)
│   └── html/index.html       # Target page
├── defense/
│   ├── rate_limit.sh         # iptables rate limiting (blocks HTTP flood)
│   ├── limit_connections.sh  # iptables connlimit (blocks slowloris)
│   └── monitor.sh            # Watch connections in real-time
└── requirements.txt
```

## Quick start

```bash
# 1. Start the target server
docker compose up -d

# 2. Install Python deps
pip install -r requirements.txt

# 3. HTTP flood attack
python lab.py http://localhost:8080

# 4. Slowloris attack (different technique — holds connections open)
python slowloris.py http://localhost:8080

# 5. Apply rate limiting defense (while flooding)
bash defense/rate_limit.sh

# 6. Apply connection limiting defense (while slowloris runs)
bash defense/limit_connections.sh
```

## What you'll learn

- **HTTP floods** — threaded GET requests overwhelm server bandwidth
- **Slowloris** — hold connections open with partial headers, exhaust connection pool
- **Rate limiting** — iptables `recent` module blocks >10 req/s per IP
- **Connection limiting** — iptables `connlimit` blocks >20 concurrent connections per IP
- **Nginx defenses** — `limit_req` and `limit_conn` at the application layer

## License

MIT — learn, experiment, defend.

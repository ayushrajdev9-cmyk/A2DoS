import requests, time, os, threading, signal, sys

target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"

running = True
stats = {
    "rps": 0, "total": 0, "status": "?", "response_ms": 0,
    "conns": 0, "defense": "off", "attack": "off"
}

def handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handler)
OS = os.name

def probe():
    while running:
        try:
            start = time.time()
            r = requests.get(target, timeout=3)
            ms = (time.time() - start) * 1000
            stats["status"] = r.status_code
            stats["response_ms"] = ms
        except requests.ConnectionError:
            stats["status"] = "DOWN"
            stats["response_ms"] = 0
        except:
            stats["status"] = "ERR"
        time.sleep(1)

threading.Thread(target=probe, daemon=True).start()

def draw():
    if OS == "nt": os.system("cls")
    else: os.system("clear")
    print("=" * 50)
    print("  A2DoS — Live Dashboard")
    print("=" * 50)
    print(f"  Target   : {target}")
    print(f"  Status   : {stats['status']}")
    print(f"  Response : {stats['response_ms']:.0f}ms" if stats['response_ms'] else "  Response : N/A")
    print("-" * 50)
    print(f"  Attacks  : {stats['attack']}")
    print(f"  Defense  : {stats['defense']}")
    if stats['attack'] != "off":
        print(f"  Total    : {stats['total']}")
        print(f"  RPS      : {stats['rps']:.0f}")
        print(f"  Conns    : {stats['conns']}")
    print("=" * 50)
    print("  Ctrl+C to exit")

try:
    while running:
        draw()
        time.sleep(1)
except KeyboardInterrupt:
    pass
print("\nDashboard closed.")

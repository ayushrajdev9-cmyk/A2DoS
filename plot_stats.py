"""Plot attack stats from CSV. Usage: python plot_stats.py <file.csv>"""
import sys, csv
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Install matplotlib: pip install matplotlib"); sys.exit(1)

file = sys.argv[1] if len(sys.argv) > 1 else "attack_log.csv"
rows = []
with open(file) as f:
    for row in csv.DictReader(f):
        rows.append(row)

if not rows:
    print("No data"); sys.exit(1)

t = [float(r["elapsed"]) for r in rows]
c = [float(r["count"]) for r in rows]
rps = [float(r["rps"]) for r in rows]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("A2DoS — Attack Stats")

ax1.plot(t, c, "b-")
ax1.set_ylabel("Count"); ax1.grid(True)

ax2.plot(t, rps, "r-")
ax2.set_xlabel("Seconds"); ax2.set_ylabel("RPS"); ax2.grid(True)

plt.tight_layout()
plt.show()

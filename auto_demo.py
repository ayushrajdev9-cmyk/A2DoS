import subprocess, sys, time, os, threading, signal

TARGET = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
OS = os.name

def run(cmd, shell=True):
    return subprocess.Popen(cmd, shell=shell)

def say(msg):
    print(f"\n{'='*60}\n>>> {msg}\n{'='*60}")
    time.sleep(2)

print("\n  A2DoS — Auto Demo")
print("  Made by Ayush Rajdev\n")

if input("Start auto-demo? (y/n): ").lower() != "y":
    print("Cancelled."); sys.exit()

say("Starting target server...")
run("docker compose up -d")
time.sleep(3)

say("Target is up. Opening dashboard in a new window...")
if OS == "nt":
    run(f'start cmd /c "python dashboard.py {TARGET}"')
else:
    run(f'x-terminal-emulator -e "python3 dashboard.py {TARGET}" &')

say("Phase 1: HTTP flood attack (15 seconds)")
attacker = run(f"python attacks.py {TARGET} http")
time.sleep(15)
attacker.terminate()

say("Target is struggling. Applying rate-limit defense...")
if OS == "nt":
    run("powershell -File defense/defend.ps1 -Action rate")
else:
    run("bash defense/rate_limit.sh")
time.sleep(2)

say("Defense active. HTTP flood is now blocked. (15 more seconds)")
attacker = run(f"python attacks.py {TARGET} http")
time.sleep(15)
attacker.terminate()

say("Phase 2: Slowloris attack (15 seconds)")
attacker = run(f"python attacks.py {TARGET} slowloris --conns 300")
time.sleep(15)
attacker.terminate()

say("Applying connection-limit defense...")
if OS == "nt":
    run("powershell -File defense/defend.ps1 -Action conn")
else:
    run("bash defense/limit_connections.sh")
time.sleep(2)

say("Both defenses active. Slowloris is now blocked. (15 seconds)")
attacker = run(f"python attacks.py {TARGET} slowloris --conns 300")
time.sleep(15)
attacker.terminate()

say("Demo complete! Summary:")
print("-" * 40)
print("  Attack types shown: HTTP flood, slowloris")
print("  Defenses shown:     rate limiting, conn limit")
print("  Lab target:         Docker Nginx on localhost")
print("-" * 40)
print("\nRevert iptables rules:")
if OS == "nt":
    print("  powershell -File defense/defend.ps1 -Action revert")
else:
    print("  bash defense/rate_limit.sh revert")
    print("  bash defense/limit_connections.sh revert")

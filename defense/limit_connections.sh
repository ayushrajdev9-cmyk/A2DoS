#!/bin/bash
# limit_connections.sh — limit concurrent connections per IP (Linux only)
# Blocks slowloris-style attacks that hold connections open
# Usage: bash limit_connections.sh [revert]

TARGET_PORT=8080

if [ "$1" = "revert" ]; then
    sudo iptables -D INPUT -p tcp --syn --dport $TARGET_PORT -m connlimit --connlimit-above 20 -j REJECT 2>/dev/null
    echo "Connection limit removed"
    exit 0
fi

sudo iptables -A INPUT -p tcp --syn --dport $TARGET_PORT -m connlimit --connlimit-above 20 -j REJECT
echo "Connection limit applied: max 20 concurrent connections per IP to port $TARGET_PORT"
echo "Revert with: bash limit_connections.sh revert"

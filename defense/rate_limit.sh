#!/bin/bash
# rate_limit.sh — apply or revert iptables rate limiting (Linux only)
# Usage: bash rate_limit.sh [revert]

TARGET_PORT=8080

if [ "$1" = "revert" ]; then
    sudo iptables -D INPUT -p tcp --dport $TARGET_PORT -m recent --update --seconds 1 --hitcount 10 -j DROP 2>/dev/null
    echo "Rate limit removed"
    exit 0
fi

sudo iptables -A INPUT -p tcp --dport $TARGET_PORT -m recent --update --seconds 1 --hitcount 10 -j DROP
echo "Rate limit applied: max 10 conn/sec to port $TARGET_PORT"
echo "Revert with: bash rate_limit.sh revert"

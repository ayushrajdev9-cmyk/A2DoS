#!/bin/bash
# monitor.sh — watch connections to the lab target (Linux only)

echo "Watching connections to port 8080 (Ctrl+C to stop)"
echo "---"
watch -n 1 "ss -tna | grep :8080 | wc -l && echo '---' && ss -tna | grep :8080 | head -20"

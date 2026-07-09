param([string]$Action = "list")

$port = 8080

if ($Action -eq "rate") {
    netsh advfirewall firewall add rule name="A2DoS_RateLimit" dir=in protocol=tcp localport=$port action=block remoteip=0.0.0.0/0
    Write-Host "[A2DoS] Rate limit applied: all inbound TCP/$port blocked" -ForegroundColor Green
}
elseif ($Action -eq "conn") {
    # Windows can't do per-IP connlimit natively, simulate by blocking new connections
    netsh advfirewall firewall add rule name="A2DoS_ConnLimit" dir=in protocol=tcp localport=$port action=block
    Write-Host "[A2DoS] Connection limit applied: inbound TCP/$port blocked" -ForegroundColor Green
}
elseif ($Action -eq "revert") {
    netsh advfirewall firewall delete rule name="A2DoS_RateLimit" 2>$null
    netsh advfirewall firewall delete rule name="A2DoS_ConnLimit" 2>$null
    Write-Host "[A2DoS] Defenses reverted" -ForegroundColor Yellow
}
elseif ($Action -eq "monitor") {
    Write-Host "Monitoring connections to port $port (Ctrl+C to stop)" -ForegroundColor Cyan
    while ($true) {
        $conns = (netstat -n | Select-String ":$port ").Count
        Write-Host "Connections: $conns"
        Start-Sleep -Seconds 2
    }
}
else {
    Write-Host "Usage: .\defend.ps1 -Action <rate|conn|revert|monitor>" -ForegroundColor Yellow
    Write-Host "  rate    - Block all inbound traffic on port $port"
    Write-Host "  conn    - Block all inbound traffic on port $port"
    Write-Host "  revert  - Remove all A2DoS firewall rules"
    Write-Host "  monitor - Watch connection count live"
}

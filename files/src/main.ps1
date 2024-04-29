using namespace System.Windows.Forms
using namespace System.Drawing
using namespace System.Collections

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

. .\settings.ps1
. .\utils.ps1
. .\gui.ps1
. .\events.ps1
. .\sprite.ps1


function Init{
    $SpawnTimer.Add_Tick($Spawn)

    $GameLoop.Start()
    $SpawnTimer.Start()
    $Window.ShowDialog() | Out-NULL
}

function End(){
    $Sprites.Reverse()
    $Projectiles.Reverse()
    @($Sprites, $Projectiles) | foreach-object{ $_ | foreach-object { $_.Dispose() } }
    
    $Score.TextAlign = [ContentAlignment]::MiddleCenter
    $Score.Top = ($Window.Height-$Score.Height)/2
}


$GameLoop.Add_Tick({
    $Score.Text = "Score: $($Settings.Score)"

    $Player.Update()

    foreach ($A in @($Sprites, $Projectiles)){
        for ([Int] $i=$A.Count-1;$i -ge 0;$i--){
            if ($A[$i].OutBounds()){
                DisposeSprite $A[$i] $A
                continue
            }

            if (($A -join ',' -eq $Sprites -join ',') -and $A[$i].GetCollision($Player)){
                $Player.Dispose()
                $GameLoop.Stop()
                Start-Sleep 1
                return End
            }

            $A[$i].Update()
        }
    }

    for ([Int] $i=$Projectiles.Count-1;$i -ge 0;$i--){
        for ([Int] $j=$Sprites.Count-1;$j -ge 0;$j--){
            if ($Projectiles[$i].GetCollision($Sprites[$j])){
                DisposeSprite $Sprites[$j] $Sprites
                DisposeSprite $Projectiles[$i] $Projectiles
                
                $Settings.Score++
                break
            }
        }
    }

    if ($Keys["W"]){ $Player.Y-=$Settings.EntitySpeed }
    if ($Keys["S"]){ $Player.Y+=$Settings.EntitySpeed }
    if ($Keys["A"]){ $Player.X-=$Settings.EntitySpeed }
    if ($Keys["D"]){ $Player.X+=$Settings.EntitySpeed }
})


Init

$Window.Dispose()
$Settings.Assets.Keys | foreach-object{ $Settings.Assets[$_].Dispose() }
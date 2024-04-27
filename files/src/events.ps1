[HashTable] $Keys = @{
    "W" = $false
    "A" = $false 
    "S" = $false 
    "D" = $false 
}

function KeyEvent{
    [OutputType([void])]
    param([KeyEventArgs] $E, [Bool] $R)

    [String] $K = $E.KeyCode

    if ($Keys.ContainsKey($K)){
        $Keys[$K] = !$R
    }
}


$Window.Add_KeyDown({
    param($_, $e)
    
    KeyEvent $e $false
})

$Window.Add_KeyUp({
    param($_, $e)
    
    if ($e.KeyCode -eq "Space"){
        return $Projectiles.Add(
            [Sprite]::new(
                "projectile.png",
                $Player.X+$Player.Element.Width,
                $Player.Y+($Player.Element.Width-$Settings.ProjectileWidth)/2,
                $Settings.ProjectileWidth,
                $Settings.ProjectileSpeed
            )
        )
    }
    KeyEvent $e $true
})
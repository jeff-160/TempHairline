function CreateTimer{
    [OutputType([Timer])]
    param([Int] $I)

    [Timer] $T = [Timer]::new()
    $T.Interval = $I
    
    return $T
}

[ScriptBlock] $Spawn = {
    [OutputType([void])]
    param()

    $Sprites.Add(
        [Sprite]::new(
            "shokam.png",
            $Window.Width-$Settings.EntitySize,
            (Get-Random -Minimum 0 -Maximum ($Window.Width-$Settings.EntitySize+1)), 
            $Settings.EntitySize,
            -$Settings.EntitySpeed
        )
    )
}

function DisposeSprite{
    [OutputType([void])]
    param([Sprite] $S, [ArrayList] $A)

    $A.Remove($S)
    $S.Dispose()
}
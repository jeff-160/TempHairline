[Form] $Window = & {
    [OutputType([Form])]

    [Form] $F = [Form]::new()
    $F.Text = $Settings.Title
    $F.Size = [Size]::new($Settings.WindowSize, $Settings.WindowSize)
    $F.BackColor = [Color]::Black
    $F.FormBorderStyle = "FixedSingle"
    $F.MaximizeBox = $false
    $F.Icon = [Icon]::new("assets\shrok.ico")

    return $F
}


[Timer] $GameLoop = CreateTimer 10
[Timer] $SpawnTimer = CreateTimer ($Settings.SpawnRate)


[Label] $Score = & {
    [OutputType([Label])]

    [Label] $L = [Label]::new()
    $L.Width, $L.Height = $Window.Width, 30
    $L.BackColor = [Color]::Transparent
    $L.ForeColor = [Color]::White
    $L.Font = [Font]::new("Arial", 15, [FontStyle]::Bold)

    return $L
}

$Window.Controls.Add($Score)
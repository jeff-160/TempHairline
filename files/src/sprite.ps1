class Sprite{
    [PictureBox] $Element
    [Int] $X; [Int] $Y
    [Int] $Speed

    Sprite([String] $Src, [Int] $X, [Int] $Y, [Int] $Width, [Int] $Speed){
        if (!$global:Settings.Assets.ContainsKey($Src)){
            $global:Settings.Assets.Add($Src, [Image]::FromFile("assets\$Src"))
        }

        $this.Element = & {
            [OutputType([PictureBox])]
            
            [PictureBox] $P = [PictureBox]::new()
            $P.Image = $global:Settings.Assets[$Src]
            $P.BackColor = [Color]::Transparent
            $P.Size = [Size]::new($Width, $Width)
            $P.SizeMode = "StretchImage"
            $P.Location = [Point]::new($global:Window.Width, 0)

            $global:Window.Controls.Add($P)
            $P.BringToFront()

            return $P
        }
        $this.X, $this.Y = $X, $Y
        $this.Speed = $Speed
    }

    [void] Update(){
        $this.X+=$this.Speed
        $this.Element.Location = [Point]::new($this.X, $this.Y)
    }

    [void] Dispose(){
        $global:Window.Controls.Remove($this.Element)
    }
    
    [Rectangle] GetBounds(){
        return [Rectangle]::FromLTRB(
            $this.X,
            $this.Y, 
            $this.X+$this.Element.Width,
            $this.Y+$this.Element.Width
        )
    }

    [Bool] GetCollision([Sprite] $S){
        return $this.GetBounds().IntersectsWith($S.GetBounds())
    }

    [Bool] OutBounds(){
        return (
            $this.X+$this.Element.Width -lt 0 -or
            $this.X -gt $global:Window.Width
        )
    }
}


[ArrayList] $Sprites = @()
[ArrayList] $Projectiles = @()

[Sprite] $Player = [Sprite]::new("player.png", 100, $Window.Height/2, $Settings.EntitySize, 0)
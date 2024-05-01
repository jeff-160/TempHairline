cd -d (Split-Path $PSCommandPath)

if (-not [Bool](tasklist | Select-String -Pattern "core.exe")){
    & .\core.exe
}
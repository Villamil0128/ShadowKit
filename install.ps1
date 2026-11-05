$ErrorActionPreference = "Stop"
$dir = "$HOME\ShadowKit"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Necesitas git. Instalalo con: winget install --id Git.Git -e" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Necesitas Python. Instalalo con: winget install --id Python.Python.3.12 -e" -ForegroundColor Red
    exit 1
}

Write-Host "[*] Clonando ShadowKit en $dir ..." -ForegroundColor Cyan
if (Test-Path $dir) {
    git -C $dir pull
} else {
    git clone https://github.com/Villamil0128/ShadowKit.git $dir
}

Write-Host "[*] Instalando dependencias (rich) ..." -ForegroundColor Cyan
pip install -r "$dir\requirements.txt" --quiet

$shim = "$env:LOCALAPPDATA\ShadowKit"
New-Item -ItemType Directory -Force -Path $shim | Out-Null
Set-Content -Path "$shim\shadowkit.bat" -Value "@echo off`r`npython `"$dir\shadowkit.py`""
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$shim*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$shim", "User")
    Write-Host "[i] shima 'shadowkit' anadida al PATH (abre una terminal nueva para usarla)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[OK] ShadowKit instalado en $dir" -ForegroundColor Green
Write-Host "Ejecuta:  shadowkit.bat  (o)  python $dir\shadowkit.py" -ForegroundColor White

#!/usr/bin/env bash
set -e
DIR="$HOME/shadowkit"

command -v git >/dev/null 2>&1 || { echo "[X] Necesitas git: sudo apt-get install -y git"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "[X] Necesitas Python 3: sudo apt-get install -y python3 python3-pip"; exit 1; }

echo "[*] Clonando ShadowKit en $DIR ..."
if [ -d "$DIR/.git" ]; then
    git -C "$DIR" pull
elif [ -d "$DIR" ]; then
    echo "[X] $DIR existe pero no es un repo de ShadowKit. Borralo o cambia DIR." >&2
    exit 1
else
    git clone https://github.com/Villamil0128/ShadowKit.git "$DIR"
fi

PYBIN=python3
echo "[*] Instalando dependencias (rich) ..."
if ! python3 -m pip install -q -r "$DIR/requirements.txt" 2>/dev/null; then
    echo "[i] pip del sistema protegido (PEP 668): creando venv ..."
    apt-get list --installed >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1 && \
        sudo apt-get install -y python3-venv >/dev/null 2>&1 || true
    python3 -m venv "$DIR/.venv"
    "$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"
    PYBIN="$DIR/.venv/bin/python3"
fi

BIN="$HOME/.local/bin"
mkdir -p "$BIN"
printf '#!/usr/bin/env bash\nexec %s "%s/shadowkit.py" "$@"\n' "$PYBIN" "$DIR" > "$BIN/shadowkit"
chmod +x "$BIN/shadowkit"
case ":$PATH:" in
    *":$BIN:"*) ;;
    *) echo "export PATH=\"$BIN:\$PATH\"" >> "$HOME/.bashrc"; echo "[i] 'shadowkit' anadida a ~/.bashrc (abre terminal nueva)";;
esac

echo ""
echo "[OK] ShadowKit instalado en $DIR"
echo "Ejecuta:  shadowkit  (o)  $PYBIN $DIR/shadowkit.py"

#!/usr/bin/env bash
set -e
DIR="$HOME/shadowkit"

command -v git >/dev/null 2>&1 || { echo "[X] Necesitas git: sudo apt-get install -y git"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "[X] Necesitas Python 3: sudo apt-get install -y python3 python3-pip"; exit 1; }

echo "[*] Clonando ShadowKit en $DIR ..."
if [ -d "$DIR" ]; then
    git -C "$DIR" pull
else
    git clone https://github.com/Villamil0128/ShadowKit.git "$DIR"
fi

echo "[*] Instalando dependencias (rich) ..."
python3 -m pip install -q -r "$DIR/requirements.txt"

BIN="$HOME/.local/bin"
mkdir -p "$BIN"
printf '#!/usr/bin/env bash\npython3 %s/shadowkit.py "$@"\n' "$DIR" > "$BIN/shadowkit"
chmod +x "$BIN/shadowkit"
case ":$PATH:" in
    *":$BIN:"*) ;;
    *) echo "export PATH=\"$BIN:\$PATH\"" >> "$HOME/.bashrc"; echo "[i] 'shadowkit' anadida a ~/.bashrc (abre terminal nueva)";;
esac

echo ""
echo "[OK] ShadowKit instalado en $DIR"
echo "Ejecuta:  shadowkit  (o)  python3 $DIR/shadowkit.py"

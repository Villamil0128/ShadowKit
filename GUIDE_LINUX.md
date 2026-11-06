# ◆ Guía de ShadowKit para Linux

Instalación, uso y mantenimiento de ShadowKit en Linux (Debian, Parrot OS, Kali, Ubuntu, Fedora...) y WSL.

## 1. Requisitos

- `git`
- `python3` + `pip` (o `python3-venv` en distros Debian/derivadas)
- Conexión a Internet para el primer arranque

Comprueba lo básico:

```bash
git --version
python3 --version
```

Si falta algo (Debian/Parrot/Kali/Ubuntu):

```bash
sudo apt-get install -y git python3 python3-pip python3-venv
```

En Fedora/RHEL: `sudo dnf install -y git python3 python3-pip`

## 2. Instalar con un solo comando

```bash
bash <(curl -sSL "https://raw.githubusercontent.com/Villamil0128/ShadowKit/main/install.sh?v=$(date +%s)")
```

Esto:

1. Clona el repo en `~/shadowkit` (o lo actualiza si ya existe)
2. Intenta instalar los requisitos con `pip`; si tu distro lo bloquea (**PEP 668** — Debian, Parrot, Kali, Ubuntu), crea automáticamente un **venv** en `~/shadowkit/.venv` e instala ahí
3. Crea el comando `shadowkit` en `~/.local/bin` (y lo añade a `~/.bashrc` si no estaba en el `PATH`)

> Si te pide contraseña de `sudo`, es para instalar `python3-venv`. Nada más.

## 3. Instalación manual (paso a paso)

Si prefieres control total:

```bash
git clone https://github.com/Villamil0128/ShadowKit.git ~/shadowkit
cd ~/shadowkit
```

Con entorno virtual (recomendado siempre):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

O instalando directo si tu distro lo permite:

```bash
python3 -m pip install -r requirements.txt
```

## 4. Cómo arrancar la app

### Con el comando global (recomendado)

```bash
shadowkit
```

> Tras instalarlo por primera vez, si no existe el comando: ejecuta `exec bash` o abre una terminal nueva para recargar el `PATH`.

### Directamente

```bash
# con venv (creado por el instalador o por ti)
~/shadowkit/.venv/bin/python3 ~/shadowkit/shadowkit.py

# sin venv
python3 ~/shadowkit/shadowkit.py
```

## 5. Modos de uso

| Comando | Qué hace |
|---|---|
| `shadowkit` | TUI interactiva completa |
| `shadowkit --list` | Lista las 46 herramientas |
| `shadowkit --check` | Qué está instalado y qué falta |
| `shadowkit --install nmap` | Instalar sin pasar por el menú |
| `shadowkit -h` | Ayuda |

Dentro de la TUI: `1` buscar · `2` categorías · `3` estado · `4` catálogo · `e` ejecutar · `i` instalar · `b/esc` atrás · `ctrl+c` salir.

Los comandos que piden privilegios de root (responder, wifite, macchanger o ettercap) ya vienen con `sudo` prefijado: te pedirá contraseña solo cuando toque.

## 6. Instalar herramientas directamente (comandos que usa la app)

Si quieres instalar alguna a mano sin entrar en la TUI:

```bash
# Escaneo de red
sudo apt-get install -y nmap masscan ncat

# Reconocimiento
sudo apt-get install -y whois
pip install sherlock-project
pip install theHarvester enum4linux-ng

# Web
sudo apt-get install -y nikto gobuster testssl.sh
git clone https://github.com/sqlmapproject/sqlmap.git ~/shadowkit/sqlmap

# Contraseñas
sudo apt-get install -y hydra john hashcat cewl
pip install hashid

# WiFi
sudo apt-get install -y aircrack-ng

# Sniffing / MITM
sudo apt-get install -y wireshark tshark tcpdump ettercap-text-only macchanger

# Forense / Estego
pip install volatility3 binwalk
sudo apt-get install -y libimage-exiftool-perl steghide

# Post-explotación
pip install netexec smbmap
sudo apt-get install -y proxychains4

# Metasploit
sudo apt-get install -y metasploit-framework

# Wordlists
git clone https://github.com/danielmiessler/SecLists.git ~/shadowkit/SecLists
```

(la app los instala igual: usa `i` en la ficha de cada herramienta)

## 7. Actualizar

```bash
# actualizar ShadowKit
bash ~/shadowkit/install.sh

# o manualmente
git -C ~/shadowkit pull

# actualizar las dependencias del venv
~/shadowkit/.venv/bin/pip install -r ~/shadowkit/requirements.txt
```

## 8. Desinstalar

```bash
rm -rf ~/shadowkit
rm -f ~/.local/bin/shadowkit
sed -i '/shadowkit/d' ~/.bashrc    # quita la línea del PATH si existe
```

## 9. Solución de problemas

| Problema | Solución |
|---|---|
| `error: externally-managed-environment` | Tu distro protege el pip del sistema (PEP 668). El instalador crea un venv automáticamente; o hazlo a mano con `python3 -m venv .venv` |
| `venv: command not found` / módulo `ensurepip` faltante | `sudo apt-get install -y python3-venv python3-full` |
| `shadowkit: command not found` | Abre una terminal nueva o `exec bash`; verifica `ls ~/.local/bin/shadowkit` y que `~/.local/bin` esté en tu `PATH` |
| Caracteres raros en la TUI | La terminal necesita UTF-8: `export LANG=C.UTF-8` o configúralo en las preferencias de tu terminal |
| `rich` no aparece aun con venv | Ejecuta con el python del venv: `~/shadowkit/.venv/bin/python3 shadowkit.py` |
| WSL | El `install.sh` funciona igual; para WiFi necesitas un adaptador externo con modo monitor y un kernel actualizado |

## 10. Nota de responsabilidad

ShadowKit une y organiza tools de ciberseguridad open source ya clásicas. Usa la app únicamente en sistemas **propios** o con **autorización expresa**. El uso sin permiso es ilegal y probablemente te de un día muy aburrido (y en la cárcel, además).

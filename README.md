<div align="center">

```
█▀█ █ █▀█ █▀▀ █ █ ▄ █ █▄ █
█▄▀ █ ▀▄▀ █▄▄ █▄▄ ▀ ▄ ▀ █ ▀█
```

# ◆ SHADOWKIT

**arsenal de pentesting en tu terminal**

`buscador en vivo` · `instalador automático` · `46 herramientas` · `windows / linux`

![python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![deps](https://img.shields.io/badge/deps-solo%20rich-black?style=flat-square)
![platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-informational?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-red?style=flat-square)

</div>

---

> "el escáner no encuentra lo que no sabe buscar. shadowkit te organiza lo que sí existe."

## Qué es

Un launcher de terminal que une en **una interfaz** las herramientas clásicas del pentesting: buscar, instalar, ejecutar y documentar, sin memorizar rutas ni googlear comandos.

- **◈ live search** — escribe y filtra instantáneo por nombre, categoría o descripción
- **◈ auto-instalador** — si la tool no está, un `i` la instala vía `winget` / `choco` / `pip` / `apt` / `git clone`
- **◈ dossier de cada tool** — qué hace, cuándo usarla, ejemplos reales
- **◈ estado del arsenal** — checklist instantáneo de qué te falta
- **◈ cero fricción** — un script de Python, única dependencia: `rich`

## Instalación

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/Villamil0128/ShadowKit/main/install.ps1 | iex
```

### Linux / macOS / WSL

```bash
bash <(curl -sSL "https://raw.githubusercontent.com/Villamil0128/ShadowKit/main/install.sh?v=$(date +%s)")
```

### Manual

```bash
git clone https://github.com/Villamil0128/ShadowKit.git
cd ShadowKit
pip install -r requirements.txt
python shadowkit.py        # windows: shadowkit.bat
```

> Guía completa de Linux (venv, PEP 668, troubleshooting): [`GUIDE_LINUX.md`](GUIDE_LINUX.md)

## En acción

```
┌──[ shadowkit ]──────────────────────────────────────┐
│                                                     │
│  ● instaladas 12/46          ◆ v2.1                 │
│                                                     │
│  › search█                                          │
│                                                     │
│  nmap              escaneo de red          ●        │
│  netexec           post-explotación        ○        │
│  nuclei            web / api               ○        │
│  ...
│                                                     │
│  ↑↓ navegar · enter abrir · esc limpiar             │
└─────────────────────────────────────────────────────┘
```

Cada ficha te da el contexto completo de la herramienta:

```
  NMAP  · escaneo de red ·  ● instalada

  CAPACIDADES
  · descubrimiento de hosts, puertos y versiones (-sV/-O)
  · +600 scripts NSE para auditar servicios sin salir de nmap

  CUÁNDO USARLA
  siempre el primer paso: saber qué expone el objetivo.

  EJEMPLOS
  $ nmap -sV -A 10.10.10.5
  $ nmap --script vuln 192.168.1.0/24
```

## El flujo

```
  recon ───→ escaneo ───→ explotación ───→ post
  amass       nmap         msfvenom       netexec
  subfinder   masscan      searchsploit   responder
  sherlock    nuclei       sqlmap         john/hashcat
```

## Arsenal (46 tools)

| Categoría | Herramientas |
|---|---|
| escaneo de red | nmap · masscan · ncat |
| reconocimiento | amass · subfinder · sherlock · theHarvester · enum4linux-ng · shodan · whois |
| web / apis | sqlmap · nikto · dirsearch · gobuster · ffuf · nuclei · whatweb · wafw00f · wpscan · testssl.sh · wfuzz · burpsuite |
| explotación | metasploit · msfvenom · searchsploit |
| post-explotación | netexec · smbmap · responder · proxychains |
| contraseñas | hydra · john · hashcat · hashid · cewl |
| wifi | aircrack-ng · wifite |
| sniffing / mitm | wireshark · tcpdump · bettercap · macchanger · ettercap |
| forense / estego | volatility3 · binwalk · exiftool · steghide |
| utilidades | SecLists |

¿falta la tuya? [abre un feature request](https://github.com/Villamil0128/ShadowKit/issues/new?template=feature_request.yml) o añádela en dos minutos ([guía](CONTRIBUTING.md#-aadir-una-herramienta-nueva)).

## Comandos rápidos

```bash
python shadowkit.py        # TUI completa
python shadowkit.py -l     # catálogo sin TUI
python shadowkit.py -c     # qué falta instalar
python shadowkit.py -i nmap sqlmap   # instala directo
```

## Roadmap

- [ ] configuración de tema (`~/.shadowkit.json`) — issue #3
- [ ] modo WSL para tools solo-linux — issue #4
- [ ] httpx y más del pipeline projectdiscovery — issue #2
- [ ] exportar hallazgos a markdown

## Estructura

```
ShadowKit/
├── shadowkit.py         lado TUI: animaciones, búsqueda, instalador, ejecutor
├── tools_registry.py    datos: 46 tools con dossier completo
├── shadowkit.bat        arranque directo windows
├── install.ps1          instalador windows
├── install.sh           instalador linux
└── requirements.txt     rich
```

## ⚠ Código de conducta

**solo en sistemas propios o con autorización expresa.** ShadowKit no crea ataques: organiza herramientas open source existentes. Tu uso es tu responsabilidad legal.

## Licencia

[MIT](LICENSE)

<div align="center">

*stay in the shadows, pentest with permission*

◆ hecho en la terminal

</div>

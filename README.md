<div align="center">

# ◆ SHADOWKIT

**Arsenal de pentesting en tu terminal — un solo script, cero configuración**

*Buscador en vivo · instalador automático · 46 herramientas · Windows / Linux*

</div>

---

## ¿Qué es?

**ShadowKit** es un launcher de terminal que reúne las herramientas esenciales de ciberseguridad ofensiva (uso **legal** y con autorización) en una sola interfaz interactiva:

- **Buscador en vivo** — escribe y filtra al instante por nombre, categoría o descripción (fuzzy search con cursor pulsante).
- **Instalador automático** — si algo no está instalado, un `i` lo instala vía `winget`, `choco`, `pip` o `git clone`.
- **Fichas completas** — cada herramienta trae *qué hace*, *cuándo usarla*, *ejemplos reales copy-paste* y su comando de instalación.
- **Ejecución con argumentos** — lanza nmap, sqlmap o hydra sin salir de ShadowKit y sin memorizar rutas.
- **Estado del arsenal** — mira de un vistazo qué tienes y qué te falta.

No hay intermediarios: es un script de Python puro con una única dependencia (`rich`).

## Pantallas

| Pantalla | Contenido |
|---|---|
| Menú principal | Acceso directo a búsqueda, categorías, estado y catálogo |
| Live search | Filtrado en vivo con `↑↓` y `enter` |
| Ficha de herramienta | Descripción, capacidades, cuándo usarla, ejemplos, instalación |
| Estado de instalaciones | Checklist por categoría de tu arsenal |

## Instalación

```bash
git clone https://github.com/Villamil0128/ShadowKit.git
cd ShadowKit
pip install -r requirements.txt
```

### Arranque

```bash
# Windows
shadowkit.bat

# Linux / macOS / WSL
python shadowkit.py
```

## Uso

| Comando | Descripción |
|---|---|
| `python shadowkit.py` | TUI interactiva completa |
| `python shadowkit.py --list` | Catálogo de las 46 herramientas |
| `python shadowkit.py --check` | Qué tienes instalado y qué falta |
| `python shadowkit.py --install nmap sqlmap` | Instala sin pasar por el menú |
| `python shadowkit.py -h` | Ayuda |

Dentro de la TUI:

| Tecla | Acción |
|---|---|
| `1` | Búsqueda en vivo |
| `2` | Explorar por categorías |
| `3` | Estado de instalaciones |
| `4` | Arsenal completo |
| `e` | Ejecutar herramienta seleccionada |
| `i` | Instalar herramienta seleccionada |
| `b` / `esc` | Volver atrás |
| `ctrl+c` | Salir |

## Qué herramientas incluye

**Escaneo de red** · nmap, masscan, ncat
**Reconocimiento** · amass, subfinder, sherlock, theHarvester, enum4linux-ng, shodan, whois
**Web / APIs** · sqlmap, nikto, dirsearch, gobuster, ffuf, nuclei, whatweb, wafw00f, wpscan, testssl.sh, wfuzz, burpsuite
**Explotación** · metasploit, msfvenom, searchsploit
**Post-explotación** · netexec, smbmap, responder, proxychains
**Contraseñas** · hydra, john, hashcat, hashid, cewl
**WiFi** · aircrack-ng, wifite
**Sniffing / MITM** · wireshark, tcpdump, bettercap, macchanger, ettercap
**Forense / Estego** · volatility3, binwalk, exiftool, steghide
**Utilidades** · SecLists

> ¿Falta tu favorita? [Abre un feature request](https://github.com/Villamil0128/ShadowKit/issues/new?template=feature_request.md) o añádela tú mismo en `tools_registry.py`.

## Estructura

```
ShadowKit/
├── shadowkit.py        Interfaz, animaciones, instalador y ejecutor
├── shadowkit.bat       Lanzador Windows
├── tools_registry.py   Catálogo: 46 herramientas con fichas completas
└── requirements.txt    Solo necesita rich
```

Añadir una herramienta nueva es copy-paste: agrega un bloque a `TOOLS` en `tools_registry.py` y aparece en el buscador automáticamente.

## Aviso legal

ShadowKit es una utilidad de organización e instalación de herramientas de ciberseguridad ya existentes y open source. Su finalidad es única y exclusivamente la prueba de seguridad ética con la **autorización expresa** de los propietarios de los sistemas analizados. El autor no se hace responsable del uso ilícito o sin autorización.

## Licencia

MIT — ver [LICENSE](LICENSE).

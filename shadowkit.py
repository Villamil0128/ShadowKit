import os
import shutil
import subprocess
import sys
import time
import random

from pathlib import Path

import rich.box as box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tools_registry import TOOLS, TOOL_CATEGORIES

if os.name == "nt":
    os.system("")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(legacy_windows=False)
TOOLS_DIR = Path.home() / "pentest-tools"

APP_NAME = "SHADOWKIT"
VERSION = "2.1"

ACCENT = "bold cyan"
DIM = "bright_black"
BODY = "bright_black"
TITLE = "bold white"
GOOD = "green"
BAD = "red"

GLITCH_CHARS = "_/#%"


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def hr(char="─", style=DIM, pad=True):
    console.print(("  " if pad else "") + f"[{style}]{char * max(0, console.width - (2 if pad else 0))}[/{style}]")


def header(path="", status=None):
    console.print()
    console.print(f"  [{ACCENT}]◆[/] [{TITLE}]SHADOWKIT[/] [{DIM}]v{VERSION}[/]", end="")
    if status is not None:
        console.print(f"    {status}", end="")
    if path:
        console.print(f"\n  [{DIM}]{path}[/bright_black]", end="")
    console.print()
    hr()


def hint_footer(text):
    console.print(f"  [{DIM}]{text}[/bright_black]")


def poll_key(timeout_ms=120):
    if os.name == "nt":
        import msvcrt

        deadline = time.time() + timeout_ms / 1000.0
        while time.time() < deadline:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\x00", "\xe0"):
                    ext = msvcrt.getwch()
                    return {"H": "\x1b[A", "P": "\x1b[B", "K": "\x1b[D", "M": "\x1b[C"}.get(ext, "")
                return ch
            time.sleep(0.005)
        return ""
    else:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ready, _, _ = select.select([sys.stdin], [], [], timeout_ms / 1000.0)
            if ready:
                return os.read(fd, 1).decode("utf-8", errors="ignore")
            return ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_key(timeout_ms=None):
    if timeout_ms is None:
        while True:
            k = poll_key(250)
            if k:
                break
    else:
        k = poll_key(timeout_ms)
    if not k:
        return "tick"
    if k == "\x03":
        raise KeyboardInterrupt
    if k in ("\r", "\n"):
        return "enter"
    if k == "\x1b":
        return "esc"
    if k in ("\x08", "\x7f"):
        return "back"
    if k == "\x1b[A":
        return "up"
    if k == "\x1b[B":
        return "down"
    if k in ("\x1b[C", "\x1b[D"):
        return "ignore"
    if len(k) == 1 and ord(k) >= 32:
        return k
    return "ignore"


def pause():
    console.input(f"\n  [{DIM}]Enter para continuar…[/bright_black]")


def boot_animation():
    clear_screen()
    console.print("\n\n\n")
    for step in range(0, console.width - 4, 4):
        clear_screen()
        console.print("\n\n\n")
        console.print("  " + "[cyan]" + "─" * step + "◆" + "[/cyan]")
        time.sleep(0.012)
    clear_screen()
    console.print("\n\n\n")
    reveal = "SHADOWKIT"
    for i in range(1, len(reveal) + 1):
        clear_screen()
        console.print("\n\n\n")
        console.print(f"  [{ACCENT}]{reveal[:i]}_[/bold cyan]")
        console.print(f"  [{DIM}]" + "▁" * len(reveal) + "[/bright_black]")
        time.sleep(0.045)
    final = f"  [{ACCENT}]{reveal}[/bold cyan]"
    clear_screen()
    console.print("\n\n\n")
    console.print(f"  [{DIM}]▁▁▁▁▁▁▁▁▁[/bright_black]")
    console.print(final)
    console.print(f"  [dim]arsenal de pentesting · v{VERSION}[/dim]")
    time.sleep(0.5)
    steps = [
        ("monitoreo de superficie", GOOD),
        ("arsenal sincronizado", GOOD),
        ("túnel listo", GOOD),
    ]
    for text, col in steps:
        console.print(f"  [{DIM}]{text:<26}[/bright_black] [bold green]·[/bold green]")
        time.sleep(0.18)
    time.sleep(0.25)
    clear_screen()


def platform_key():
    return "windows" if os.name == "nt" else "linux"


def tools_dir_str():
    return str(TOOLS_DIR)


def is_installed(tool):
    check = tool.get("check")
    if not check:
        return False
    candidate = TOOLS_DIR / check
    if candidate.exists():
        return True
    exe = check.split("\\")[0].split("/")[0]
    return shutil.which(exe) is not None


def install_commands(tool):
    return tool.get("install", {}).get(platform_key(), [])


def status_dot(tool):
    check = tool.get("check")
    if not check:
        return "[cyan]◦ gui[/cyan]"
    return "[green]●[/green] [green]instalada[/green]" if is_installed(tool) else "[red]○[/red] [red]no instalada[/red]"


def status_dot_inline(tool):
    check = tool.get("check")
    if not check:
        return "[cyan]◦[/cyan]"
    return "[green]●[/green]" if is_installed(tool) else "[red]○[/red]"


def fuzzy_score(query, tool):
    if not query.strip():
        return 1
    haystack = " ".join([tool["name"], tool["category"], tool.get("desc", ""), tool.get("use", "")]).lower()
    q = query.lower().strip()
    score = 0
    for part in q.split():
        if part in tool["name"].lower():
            score += 12
        elif part in haystack:
            idx = haystack.find(part)
            score += max(2, 8 - idx // 30)
        else:
            pos = 0
            hits = 0
            for char in part:
                idx = haystack.find(char, pos)
                if idx == -1:
                    hits = 0
                    break
                hits += 1
                pos = idx + 1
            score += hits
    return score


def matches(query):
    scored = [(fuzzy_score(query, t), t) for t in TOOLS]
    good = [(s, t) for s, t in scored if s > 0]
    good.sort(key=lambda p: (-p[0], p[1]["name"]))
    return [t for _, t in good]


def paint_search(query, results, index, blink_on):
    clear_screen()
    header(path="búsqueda")
    console.print()
    cursor = "[cyan]▌[/cyan]" if blink_on else "[dim] [/dim]"
    console.print(f"  [{ACCENT}]›[/] [{TITLE}]{query}[/]" + (cursor if query else ""))
    if not query:
        console.print(f"  [{DIM}]escribe para filtrar por nombre, categoría o descripción…[/bright_black]")
    console.print()
    visible = results[:12]
    if not visible and query:
        console.print(f"  [{DIM}]sin coincidencias[/bright_black]")
    for i, tool in enumerate(visible):
        if i == index:
            console.print(f"  [cyan]▌[/] [bold white]{tool['name']:<16}[/] [{DIM}]{tool['category']:<26}[/bright_black] {status_dot_inline(tool)}")
        else:
            console.print(f"   [bright_black]{tool['name']:<16}[/bright_black] [dim]{tool['category']:<26}[/dim] {status_dot_inline(tool)}")
    if len(results) > 12:
        console.print(f"   [{DIM}]… +{len(results) - 12} más[/bright_black]")
    console.print()
    hint_footer("↑↓ navegar · enter abrir · esc limpiar · ctrl+c salir")


def live_search():
    query = ""
    index = 0
    blink_on = True
    results = matches(query)
    while True:
        paint_search(query, results, index, blink_on)
        key = read_key(timeout_ms=450)
        if key == "tick":
            blink_on = not blink_on
            continue
        blink_on = True
        if key == "up":
            if results:
                index = (index - 1) % min(len(results), 12)
        elif key == "down":
            if results:
                index = (index + 1) % min(len(results), 12)
        elif key == "enter":
            if results:
                return results[min(index, len(results) - 1)]
        elif key == "esc":
            if query:
                query = ""
                index = 0
                results = matches(query)
            else:
                return None
        elif key == "back":
            query = query[:-1]
            index = 0
            results = matches(query)
        elif key == "ignore":
            pass
        else:
            query += key
            index = 0
            results = matches(query)


def show_tool_info(tool):
    console.print(f"  [{TITLE}]{tool['name'].upper()}[/]  [{DIM}]· {tool['category']} ·[/]  {status_dot(tool)}")
    console.print()
    console.print(f"  [{BODY}]{tool.get('desc', '')}[/bright_black]")
    console.print()
    if tool.get("features"):
        console.print(f"  [{ACCENT}]CAPACIDADES[/]")
        for f in tool["features"]:
            console.print(f"  [cyan]·[/] [{BODY}]{f}[/bright_black]")
        console.print()
    if tool.get("use"):
        console.print(f"  [{ACCENT}]CUÁNDO USARLA[/]")
        console.print(f"  [{BODY}]{tool['use']}[/bright_black]")
        console.print()
    if tool.get("notes"):
        console.print(f"  [yellow]! {tool['notes']}[/yellow]")
        console.print()
    if tool.get("examples"):
        console.print(f"  [{ACCENT}]EJEMPLOS[/]")
        for example in tool["examples"]:
            console.print(f"  [{DIM}]$[/bright_black] [green]{example}[/green]")
        console.print()
    cmds = install_commands(tool)
    console.print(f"  [{ACCENT}]INSTALACIÓN ({platform_key()})[/]")
    if cmds:
        for command in cmds:
            console.print(f"  [{DIM}]$ [/][magenta]{command.replace('{dir}', tools_dir_str())}[/magenta]")
    else:
        console.print(f"  [{DIM}]sin instalador automático en esta plataforma[/bright_black]")
    console.print()


def resolve_command(tool, args=""):
    base = tool.get("base")
    if not base:
        return None
    command = base.replace("{py}", sys.executable)
    command = command.replace("{dir}", tools_dir_str())
    if args:
        command = f"{command} {args}"
    return command


def run_tool(tool):
    clear_screen()
    header(f"búsqueda › {tool['name']} › ejecutar")
    show_tool_info(tool)
    if not tool.get("base"):
        console.print(f"\n  [yellow]Esta herramienta es gráfica o es un recurso: instálala y ábrela por su cuenta.[/yellow]")
        pause()
        return
    args = console.input(f"  [{ACCENT}]›[/] argumentos (vacío = mostrar ayuda de la herramienta): ").strip()
    command = resolve_command(tool, args)
    console.print(f"\n  [{DIM}]$[/] [green]{command}[/green]")
    confirm = console.input(f"  ¿ejecutar? [green]s[/green]/N: ").strip().lower()
    if confirm == "s":
        console.print("\n")
        cwd = TOOLS_DIR / tool["cwd"] if tool.get("cwd") else None
        try:
            subprocess.run(command, shell=True, cwd=cwd)
        except Exception as exc:
            console.print(f"  [red]error: {exc}[/red]")
    pause()


def install_tool(tool):
    clear_screen()
    header(f"búsqueda › {tool['name']} › instalar")
    show_tool_info(tool)
    cmds = install_commands(tool)
    if not cmds:
        console.print(f"\n  [yellow]Sin instalación automática para {platform_key()}. Hazlo a mano con los comandos del panel superior.[/yellow]")
        pause()
        return
    if is_installed(tool):
        re_i = console.input("  Ya está instalada. ¿reinstalar/actualizar? y/N: ").strip().lower()
        if re_i != "y":
            return
    for command in cmds:
        prepared = command.replace("{dir}", tools_dir_str())
        console.print(f"\n  [cyan]›[/] [magenta]{prepared}[/magenta]\n")
        try:
            subprocess.run(prepared, shell=True)
        except Exception as exc:
            console.print(f"  [red]fallo: {exc}[/red]")
        if is_installed(tool):
            break
    if is_installed(tool):
        console.print(f"\n  [bold green]✔ {tool['name']} lista[/bold green]")
    else:
        console.print(f"\n  [bold red]✘ no se pudo verificar la instalación[/bold red]")
    pause()


def tool_action_loop(tool):
    while True:
        clear_screen()
        header(f"búsqueda › {tool['name']}")
        show_tool_info(tool)
        hint_footer("e ejecutar · i instalar · b/esc volver · ctrl+c salir")
        key = read_key().lower()
        if key == "e":
            run_tool(tool)
        elif key == "i":
            install_tool(tool)
        elif key in ("b", "esc"):
            return


def menu_selector(items, title, breadcrumb="menu"):
    idx = 0
    while True:
        clear_screen()
        header(breadcrumb, status=f"[{DIM}]{idx + 1}/{len(items)}[/bright_black]")
        console.print(f"  [{ACCENT}]{title.upper()}[/]")
        console.print()
        for i, item in enumerate(items):
            if i == idx:
                console.print(f"  [cyan]▌[/] [bold white]{item['label']}[/]")
            else:
                console.print(f"   [{DIM}]{item['label']}[/bright_black]")
        console.print()
        hint_footer("↑↓ navegar · enter elegir · esc atrás")
        key = read_key()
        if key == "up":
            idx = (idx - 1) % len(items)
        elif key == "down":
            idx = (idx + 1) % len(items)
        elif key == "enter":
            return idx
        elif key == "esc":
            return None


def browse_categories():
    counts = {c: sum(1 for t in TOOLS if t["category"] == c) for c in TOOL_CATEGORIES}
    items = [{"label": f"{c}  [bright_black]({counts[c]})[/bright_black]"} for c in TOOL_CATEGORIES]
    sel = menu_selector(items, "explorar · categorías", "categorías")
    if sel is None:
        return None
    category = TOOL_CATEGORIES[sel]
    tools = [t for t in TOOLS if t["category"] == category]
    items2 = [{"label": f"{t['name']}  [bright_black]{t['desc'][:44]}…[/bright_black]"} for t in tools]
    sel2 = menu_selector(items2, category.lower(), f"categorías › {category}")
    if sel2 is None:
        return None
    return tools[sel2]


def show_installed():
    clear_screen()
    ok_count = sum(1 for t in TOOLS if is_installed(t))
    header("estado", status=f"[green]{ok_count}[/green][bright_black]/{len(TOOLS)}[/bright_black]")
    console.print()
    grouped = {}
    for tool in TOOLS:
        grouped.setdefault(tool["category"], []).append(tool)
    for cat in TOOL_CATEGORIES:
        tools = grouped.get(cat, [])
        if not tools:
            continue
        console.print(f"  [{ACCENT}]{cat.upper()}[/]")
        for tool in tools:
            console.print(f"    [{BODY}]{tool['name']:<16}[/bright_black] {status_dot_inline(tool)}")
        console.print()
    pause()


def list_catalog():
    clear_screen()
    header("arsenal completo", status=f"[{DIM}]{len(TOOLS)} herramientas[/bright_black]")
    console.print()
    for category in TOOL_CATEGORIES:
        tools = [t for t in TOOLS if t["category"] == category]
        if not tools:
            continue
        console.print(f"  [{ACCENT}]{category.upper()}[/]")
        for tool in tools:
            console.print(f"    [{BODY}]{tool['name']:<16}[/bright_black] [{DIM}]{tool['desc'][:70]}…[/bright_black] {status_dot_inline(tool)}")
        console.print()
    pause()


def main_menu():
    while True:
        clear_screen()
        total_ok = sum(1 for t in TOOLS if is_installed(t))
        header(status=f"[green]{total_ok}[/green][bright_black]/ arsenal listo[/bright_black]")
        console.print()
        options = [
            ("buscar herramienta", "live search"),
            ("explorar por categorías", f"{len(TOOL_CATEGORIES)} categorías"),
            ("estado de instalaciones", f"{total_ok}/{len(TOOLS)}"),
            ("arsenal completo", "catálogo y detalles"),
        ]
        console.print("  elige una acción:\n")
        for i, (label, sub) in enumerate(options, 1):
            console.print(f"  [{ACCENT}]{i}[/] [{TITLE}]{label}[/] [{DIM}]· {sub}[/bright_black]")
        console.print(f"\n  [{ACCENT}]q[/] [{TITLE}]salir[/]")
        console.print()
        hint_footer("usa el número en pantalla o ctrl+c para salir")
        key = read_key()
        if key == "1":
            tool = live_search()
            if tool:
                tool_action_loop(tool)
        elif key == "2":
            tool = browse_categories()
            if tool:
                tool_action_loop(tool)
        elif key == "3":
            show_installed()
        elif key == "4":
            list_catalog()
        elif key in ("q", "Q", "esc"):
            clear_screen()
            console.print("\n\n")
            console.print(f"  [{ACCENT}]◆ SHADOWKIT[/] [{DIM}]saliendo… usa solo sobre objetivos autorizados[/bright_black]")
            time.sleep(0.6)
            clear_screen()
            return


def cli_list():
    table = Table(box=box.MINIMAL)
    table.add_column("herramienta", style="bold")
    table.add_column("categoría")
    table.add_column("estado")
    for tool in sorted(TOOLS, key=lambda t: (t["category"], t["name"])):
        ok = "si" if is_installed(tool) else "no"
        table.add_row(tool["name"], tool["category"], ok)
    console.print(table)


def cli_check():
    missing, present = [], []
    for tool in TOOLS:
        (present if is_installed(tool) else missing).append(tool)
    console.print("[green]● instaladas ({0}):[/green] {1}".format(len(present), ", ".join(t["name"] for t in present)))
    console.print("[red]○ faltan ({0}):[/red] {1}".format(len(missing), ", ".join(t["name"] for t in missing)))


def cli_install(names):
    for name in names:
        tool = next((t for t in TOOLS if t["name"].lower() == name.lower()), None)
        if not tool:
            console.print(f"[red]✘ desconocida: {name}[/red]")
            continue
        console.print(f"[cyan]› instalando {tool['name']}...[/cyan]")
        cmds = install_commands(tool)
        if not cmds:
            console.print("  [yellow]sin instalador automático en esta plataforma.[/yellow]")
            continue
        for command in cmds:
            subprocess.run(command.replace("{dir}", tools_dir_str()), shell=True)
            if is_installed(tool):
                break
        console.print("  [green]✔ lista[/]" if is_installed(tool) else "  [red]✘ no verificada[/]")


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-l", "--list"):
        cli_list()
        return
    if args and args[0] in ("-c", "--check"):
        cli_check()
        return
    if args and args[0] in ("-i", "--install"):
        cli_install(args[1:] or [])
        return
    if args and args[0] in ("-h", "--help"):
        console.print(f"[bold cyan]◆ SHADOWKIT v{VERSION}[/bold cyan]")
        console.print("  python shadowkit.py                      TUI interactiva")
        console.print("  python shadowkit.py --list               catálogo")
        console.print("  python shadowkit.py --check              estado de instalación")
        console.print("  python shadowkit.py --install nmap       instalar sin menú")
        return
    try:
        boot_animation()
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        console.print(f"\n  [{ACCENT}]◆ SHADOWKIT[/] [{DIM}]conexión interrumpida[/bright_black]\n")


if __name__ == "__main__":
    main()

# Guía de contribución a ShadowKit

¡Gracias por querer sumar! Todo aporte es bienvenido, desde corregir un ejemplo hasta añadir herramientas nuevas.

## Cómo contribuir

1. **Fork** del repositorio.
2. Crea una rama con nombre descriptivo:
   ```bash
   git checkout -b feature/nombre-del-cambio
   ```
3. Realiza tus cambios.
4. Verifica que la app arranca y no rompe nada:
   ```bash
   python shadowkit.py          # TUI
   python shadowkit.py --check  # estado
   ```
5. Commit claro y conciso ("Añade herramienta netscanner").
6. Abre un **Pull Request** a `main`.

## Añadir una herramienta nueva

Edita `tools_registry.py` y agrega un objeto a la lista `TOOLS`:

```python
{
    "name": "netscanner",
    "category": "Escaneo de red",           # debe existir en TOOL_CATEGORIES
    "desc": "Descripción corta (una frase).",
    "features": ["capacidad 1", "capacidad 2", "capacidad 3"],
    "use": "Cuándo conviene usarla (una frase).",
    "check": "netscanner",                   # binario o ruta relativa a ~/pentest-tools
    "base": "netscanner",                    # comando base; usa {py} y {dir} como placeholders
    "install": {
        "windows": ["winget install ..."],   # winget / choco / pip / git clone
        "linux": ["sudo apt-get install -y netscanner"],
    },
    "examples": ["netscanner -sV 10.10.10.5"],
    "notes": "Advertencia opcional.",         # opcional
}
```

Reglas para el catálogo:

- ES-ES: descripciones, `features` y ejemplos en español.
- La herramienta debe ser legítima y open source, y útil para pentesting ético.
- `check`, `base` y `install` son obligatorios. Si corre en otra ubicación, usa `cwd`.
- Verifica al menos que `--check` detecte la herramienta y que un ejemplo sea válido.

## Convenciones de código

- Python 3.8+, stdlib + `rich` nada más.
- Sin comentarios innecesarios: el código debe ser autoexplicativo.
- Estilo visual de la TUI:
  - Acento: `[bold cyan]`
  - Texto secundario: `bright_black`
  - UX: flechas para navegar, `enter` para elegir, `esc` para atrás, `ctrl+c` para salir.
- Las secciones de pantallas van en MAYÚSCULAS (CAPACIDADES, EJEMPLOS...).

## Reporte de bugs y features

Usa las plantillas de issues:
- [Bug report](https://github.com/Villamil0128/ShadowKit/issues/new?template=bug_report.yml)
- [Feature request](https://github.com/Villamil0128/ShadowKit/issues/new?template=feature_request.yml)

## Código de conducta

Sé respetuoso y profesional. Este proyecto existe para la ciberseguridad ética: no se aceptan contribuciones que faciliten ataques sin autorización explícita.

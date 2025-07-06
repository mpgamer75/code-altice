# Generador de Reportes de Seguridad

Este proyecto es una herramienta de escritorio y de línea de comandos diseñada para procesar archivos de registros de seguridad (en formato Excel o CSV), extraer información relevante sobre fallos de inicio de sesión y generar reportes de texto consolidados.

## ✨ Características

- **Interfaz Gráfica Moderna**: Una GUI intuitiva y fácil de usar construida con `ttkbootstrap`.
- **Procesamiento Dual**: Soporta tanto archivos de Excel (`.xls`, `.xlsx`) como de CSV (`.csv`).
- **Procesamiento en Lote**: Procesa todos los archivos válidos encontrados en la carpeta de entrada.
- **Reportes Personalizados**: Genera reportes intermedios con datos extraídos y reportes finales con un formato de mensaje predefinido.
- **Modo CLI**: Opción para ejecutar el procesador desde la línea de comandos para automatización y scripting.
- **Configuración Persistente**: Guarda las rutas de entrada/salida para mayor comodidad.
- **Empaquetado Sencillo**: Mínimas dependencias y un lanzador que verifica si están instaladas.

## 📋 Prerrequisitos

- Python 3.7 o superior.
- `pip` para instalar las dependencias.
- `tkinter` (generalmente incluido en las instalaciones estándar de Python).

## 🛠️ Instalación

1. **Clona o descarga el proyecto** en tu máquina local.
2. **Abre una terminal** en el directorio raíz del proyecto.
3. **Instala las dependencias** ejecutando el siguiente comando:

    ```bash
    pip install -r requirements.txt
    ```

    También puedes usar el lanzador para verificar las dependencias:

    ```bash
    python launcher.py --check
    ```

## 🚀 Uso

La aplicación se puede lanzar en modo de interfaz gráfica (GUI) o en modo de línea de comandos (CLI).

### 🖥️ Modo GUI

Para lanzar la interfaz gráfica, simplemente ejecuta `launcher.py` sin argumentos:

```bash
python launcher.py
```

**Funcionalidades de la GUI:**

1. **Configuración de Rutas**:
    - **Carpeta de Entrada**: Especifica la carpeta donde se encuentran tus archivos `.xls`, `.xlsx` o `.csv`. Puedes usar el botón `Explorar`.
    - **Carpeta de Salida**: Especifica dónde se guardarán los reportes finales.
    - **Añadir Archivo**: Copia fácilmente uno o más archivos a la carpeta de entrada.

2. **Acciones**:
    - **Procesar Archivos**: Inicia el proceso de generación de reportes. La barra de progreso mostrará el estado.
    - **Abrir Carpeta de Salida**: Abre la carpeta de reportes generados en tu explorador de archivos.
    - **Actualizar Estado**: Refresca el conteo de archivos de entrada y reportes generados.

3. **Registro de Actividad**: Muestra en tiempo real los logs del proceso.

### ⌨️ Modo CLI

Para usar la herramienta desde la terminal, utiliza el flag `--cli`.

```bash
# Procesar con las carpetas por defecto (xls_folder y rapport2)
python launcher.py --cli

# Especificar carpetas de entrada y salida personalizadas
python launcher.py --cli --input ./mis_datos --output ./mis_reportes
```

## 📁 Formato de Archivos de Entrada

### Archivos Excel (`.xls`, `.xlsx`)

La herramienta espera que los archivos de Excel tengan una estructura específica:

- **Metadatos de Cabecera**: Las primeras 9-11 filas contienen información como "Report Name", "Period", etc.
- **Datos Tabulares**: La tabla de datos debe comenzar a partir de la fila 12.
- **Columnas de Interés**:
  - La **columna B** (índice 1) debe contener las **direcciones IP** del cliente.
  - La **columna G** (índice 6) debe contener la **razón** del fallo.

### Archivos CSV (`.csv`)

- El archivo debe tener una fila de encabezado.
- La herramienta buscará las columnas `Client IP` y `Reason` por su nombre.
- Si no las encuentra, usará un fallback a las posiciones de columna:
  - La **segunda columna** (índice 1) para las **IPs**.
  - La **séptima columna** (índice 6) para las **razones**.

Se incluye un archivo `sample_report.csv` en la carpeta `xls_folder` para que puedas probar la aplicación inmediatamente.

## 🏗️ Estructura del Proyecto

```
.
├── automated_reports.py    # Lógica principal de procesamiento de reportes
├── config.json             # Archivo de configuración para la GUI
├── gui_app.py              # Implementación de la interfaz gráfica
├── launcher.py             # Script de lanzamiento (GUI y CLI)
├── process_reports.log     # Archivo de log principal
├── requirements.txt        # Dependencias del proyecto
├── xls_folder/             # Carpeta de entrada por defecto
│   └── sample_report.csv   # Archivo de ejemplo
└── rapport2/               # Carpeta de salida por defecto (creada por la app)
```

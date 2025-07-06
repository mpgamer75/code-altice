#!/usr/bin/env python3
"""
Script de lanzamiento para el Generador de Reportes de Seguridad.
"""

import sys
import os
import argparse
from pathlib import Path

def check_dependencies():
    """Verifica si las dependencias requeridas están instaladas."""
    # tkinter no se instala vía pip, por eso se maneja diferente.
    required_packages = {'pandas': 'pandas', 'openpyxl': 'openpyxl', 'ttkbootstrap': 'ttkbootstrap'}
    missing_packages = []
    
    for pkg_import, pkg_install in required_packages.items():
        try:
            __import__(pkg_import)
        except ImportError:
            missing_packages.append(pkg_install)
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append("tkinter")

    if missing_packages:
        print("❌ Dependencias faltantes:")
        for package in missing_packages:
            print(f"  - {package}")
        
        pip_packages = [p for p in missing_packages if p != "tkinter"]
        if pip_packages:
            print("\n📦 Para instalarlas, usa el siguiente comando:")
            print(f"pip install {' '.join(pip_packages)}")

        if 'tkinter' in missing_packages:
            print("\nNota: tkinter no fue encontrado. Usualmente viene incluido con Python.")
            print("Asegúrate de que tu instalación de Python no sea una versión 'headless' o mínima.")
        return False
    return True

def run_gui():
    """Lanza la aplicación en modo de interfaz gráfica (GUI)."""
    try:
        from gui_app import main as gui_main
        print("🚀 Iniciando la interfaz gráfica...")
        gui_main()
    except Exception as e:
        print(f"❌ Error al iniciar la interfaz gráfica: {e}")
        sys.exit(1)

def run_cli(input_dir, output_dir):
    """Ejecuta la aplicación en modo de línea de comandos (CLI)."""
    try:
        from automated_reports import ReportProcessor
        
        print("🚀 Iniciando el procesamiento en modo de línea de comandos...")
        processor = ReportProcessor(input_dir=input_dir, output_dir=output_dir)
        results = processor.run()
        
        print(f"\n🎯 ¡Procesamiento completado!")
        print(f"📊 {len(results['processed'])} archivos procesados")
        print(f"❌ {len(results['failed'])} archivos con errores")
        print(f"⏱️ Duración: {results['duration']}")
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")
        sys.exit(1)

def main():
    """Función principal del lanzador."""
    parser = argparse.ArgumentParser(
        description="Generador de Reportes de Seguridad.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python launcher.py                                # Lanza la interfaz gráfica (GUI)
  python launcher.py --cli                          # Lanza en modo de línea de comandos (CLI)
  python launcher.py --cli --input data --output reports    # Personaliza las carpetas de entrada/salida
        """
    )
    
    parser.add_argument('--cli', action='store_true', 
                       help='Ejecutar en modo de línea de comandos (CLI).')
    parser.add_argument('--input', default='xls_folder', 
                       help='Carpeta de entrada para los archivos a procesar (por defecto: xls_folder).')
    parser.add_argument('--output', default='rapport2', 
                       help='Carpeta de salida para los reportes generados (por defecto: rapport2).')
    parser.add_argument('--check', action='store_true', 
                       help='Verifica las dependencias y termina.')
    
    args = parser.parse_args()
    
    print("📋 Generador de Reportes de Seguridad")
    print("=" * 40)
    
    if args.check:
        if check_dependencies():
            print("\n✅ Todas las dependencias requeridas están instaladas.")
        sys.exit(0 if check_dependencies() else 1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Lancer l'application
    if args.cli:
        run_cli(args.input, args.output)
    else:
        run_gui()

if __name__ == "__main__":
    main()
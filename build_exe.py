"""
Script de build pour créer un exécutable autonome du Generador de Reportes de Seguridad.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Vérifie si PyInstaller est installé."""
    try:
        import PyInstaller
        print("✅ PyInstaller trouvé")
        return True
    except ImportError:
        print("❌ PyInstaller non trouvé")
        return False

def install_pyinstaller():
    """Installe PyInstaller."""
    print("📦 Installation de PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installé avec succès")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation de PyInstaller")
        return False

def create_spec_file():
    """Crée le fichier .spec pour PyInstaller."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Collecter les données des packages essentiels
ttkbootstrap_datas = collect_data_files('ttkbootstrap')

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('automated_reports.py', '.'),
        ('gui_app.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('xls_folder', 'xls_folder'),
    ] + ttkbootstrap_datas,
    hiddenimports=[
        'ttkbootstrap',
        'ttkbootstrap.constants',
        'ttkbootstrap.scrolled',
        'pandas',
        'openpyxl',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'threading',
        'queue',
        'logging'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'IPython',
        'matplotlib',
        'scipy',
        'numpy.distutils',
        'numpy.f2py',
        'pandas.plotting',
        'pandas.tests',
        'test',
        'tests',
        'unittest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GeneradorReportesSeguridad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='version_info.txt'
)
'''
    
    with open('app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✅ Fichier .spec créé")

def create_version_info():
    """Crée le fichier d'informations de version."""
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Altice'),
        StringStruct(u'FileDescription', u'Generador de Reportes de Seguridad'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'GeneradorReportesSeguridad'),
        StringStruct(u'LegalCopyright', u'© 2025 Altice'),
        StringStruct(u'OriginalFilename', u'GeneradorReportesSeguridad.exe'),
        StringStruct(u'ProductName', u'Generador de Reportes de Seguridad'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print("✅ Fichier d'informations de version créé")

def build_executable():
    """Construit l'exécutable avec PyInstaller."""
    print("🔨 Construction de l'exécutable...")
    
    # Nettoyer les builds précédents
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    try:
        # Construire avec PyInstaller
        subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            "app.spec"
        ], check=True)
        
        print("✅ Exécutable créé avec succès!")
        
        # Créer le dossier de distribution final
        dist_dir = Path("GeneradorReportesSeguridad_Portable")
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        dist_dir.mkdir()
        
        # Copier l'exécutable
        shutil.copy2("dist/GeneradorReportesSeguridad.exe", dist_dir)
        
        # Créer les dossiers nécessaires
        (dist_dir / "xls_folder").mkdir(exist_ok=True)
        (dist_dir / "rapport2").mkdir(exist_ok=True)
        (dist_dir / "reports").mkdir(exist_ok=True)
        
        # Copier les fichiers importants
        shutil.copy2("README.md", dist_dir)
        
        # Créer un fichier d'instructions
        instructions = """
GENERADOR DE REPORTES DE SEGURIDAD
==================================

INSTRUCCIONES DE USO:
1. Ejecute GeneradorReportesSeguridad.exe
2. La aplicación se iniciará automáticamente
3. Use "Añadir Archivos" para cargar archivos Excel/CSV
4. Haga clic en "Extraer Información" para procesar
5. Haga clic en "Generar Informes Finales" para crear reportes

CARPETAS:
- xls_folder: Coloque aquí sus archivos Excel/CSV
- rapport2: Los informes finales se guardarán aquí
- reports: Carpeta temporal para reportes intermedios

SOPORTE:
- Para reportar problemas, contacte al administrador del sistema
- Este ejecutable incluye todas las dependencias necesarias

© 2025 Altice
"""
        
        with open(dist_dir / "INSTRUCCIONES.txt", "w", encoding="utf-8") as f:
            f.write(instructions)
        
        print(f"✅ Paquete portable creado en: {dist_dir}")
        print(f"📁 Tamaño del ejecutable: {os.path.getsize(dist_dir / 'GeneradorReportesSeguridad.exe') / 1024 / 1024:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction: {e}")
        return False

def cleanup():
    """Nettoie les fichiers temporaires."""
    print("🧹 Nettoyage des fichiers temporaires...")
    
    files_to_remove = ['app.spec', 'version_info.txt']
    dirs_to_remove = ['build', '__pycache__']
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
    
    for dir in dirs_to_remove:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    print("✅ Nettoyage terminé")

def main():
    """Fonction principale du script de build."""
    print("🏗️ GENERADOR DE REPORTES DE SEGURIDAD - BUILD SCRIPT")
    print("=" * 60)
    
    # Vérifier PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("❌ Impossible d'installer PyInstaller")
            return False
    
    # Créer les fichiers de configuration
    create_spec_file()
    create_version_info()
    
    # Construire l'exécutable
    if build_executable():
        print("\n🎉 BUILD TERMINÉ AVEC SUCCÈS!")
        print("📦 Votre application portable est prête dans le dossier 'GeneradorReportesSeguridad_Portable'")
        print("💾 Vous pouvez maintenant distribuer ce dossier à vos collègues")
        print("🚀 Ils n'auront qu'à exécuter 'GeneradorReportesSeguridad.exe' pour lancer l'application")
    else:
        print("\n❌ ERREUR LORS DU BUILD")
        return False
    
    # Nettoyer
    cleanup()
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nAppuyez sur Entrée pour fermer...")
    sys.exit(0 if success else 1) 
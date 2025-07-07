@echo off
chcp 65001 >nul
title Construcción del Ejecutable - Generador de Reportes de Seguridad
color 0A

echo.
echo ===============================================
echo   CONSTRUCCIÓN DEL EJECUTABLE
echo   Generador de Reportes de Seguridad
echo ===============================================
echo.

echo ℹ️  Este script creará un archivo .exe portable que incluye
echo    todas las dependencias necesarias para la aplicación.
echo.
echo ⚠️  IMPORTANTE: Este proceso puede tardar varios minutos
echo    y requerirá descargar PyInstaller si no está instalado.
echo.

set /p choice="¿Desea continuar? (S/N): "
if /i "%choice%" neq "S" (
    echo.
    echo ❌ Proceso cancelado por el usuario
    pause
    exit /b 0
)

echo.
echo 🚀 Iniciando construcción del ejecutable...
echo.

REM Ejecutar el script de construcción
python build_exe.py

echo.
echo ✅ Proceso terminado
echo.
echo 📁 Si el proceso fue exitoso, encontrará el ejecutable en:
echo    GeneradorReportesSeguridad_Portable\GeneradorReportesSeguridad.exe
echo.

pause 
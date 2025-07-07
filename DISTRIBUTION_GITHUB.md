# 📦 Distribution via GitHub Releases

## 🎯 Objectif

Ce guide explique comment distribuer l'exécutable `GeneradorReportesSeguridad.exe` via GitHub Releases, permettant de télécharger facilement l'application depuis n'importe quel ordinateur.

## 📋 Étapes pour créer une Release

### 1. Préparer l'Archive
```bash
# Compresser le dossier portable
7z a GeneradorReportesSeguridad_v1.0.zip GeneradorReportesSeguridad_Portable/
```

### 2. Sur GitHub
1. **Aller** à votre repository
2. **Cliquer** sur "Releases" (à droite)
3. **Cliquer** "Create a new release"
4. **Remplir** :
   - Tag version: `v1.0.0`
   - Release title: `Generador de Reportes de Seguridad v1.0`
   - Description: voir ci-dessous

### 3. Description de la Release
```markdown
## 📊 Generador de Reportes de Seguridad v1.0

### ✨ Características
- ✅ Procesamiento de archivos Excel/CSV
- ✅ Generación automática de reportes
- ✅ Interfaz gráfica moderna
- ✅ Portátil - no requiere instalación

### 📥 Descarga e Instalación
1. Descargue `GeneradorReportesSeguridad_v1.0.zip`
2. Extraiga el archivo ZIP
3. Ejecute `GeneradorReportesSeguridad.exe`

### 💻 Requisitos del Sistema
- Windows 10/11 (64-bit)
- Mínimo 100 MB de espacio libre
- NO requiere Python ni dependencias

### 🚀 Uso Rápido
1. Añadir archivos Excel/CSV
2. Extraer información
3. Generar informes finales
4. Acceder a resultados en carpeta `rapport2`

### 🐛 Soporte
Para problemas técnicos, abrir un Issue en este repository.
```

### 4. Adjuntar le Archivo
- **Arrastrar** le fichier ZIP à la zone "Attach binaries"
- **Cliquer** "Publish release"

## 🔄 Pour Mettre à Jour

### Nouvelle Version
1. **Reconstruire** l'exécutable si nécessaire
2. **Créer** une nouvelle archive
3. **Créer** une nouvelle release (v1.1, v1.2, etc.)

### Scripts Utiles
```bash
# Reconstruire l'exécutable
python build_exe.py

# Créer l'archive
7z a GeneradorReportesSeguridad_v1.1.zip GeneradorReportesSeguridad_Portable/
```

## 📊 Avantages GitHub Releases

✅ **Historique des versions** - Suivi des mises à jour  
✅ **Download stats** - Voir combien de téléchargements  
✅ **Fichiers volumineux** - Jusqu'à 2GB par fichier  
✅ **URLs stables** - Liens permanents pour télécharger  
✅ **Automatisation** - Possibilité d'automatiser via GitHub Actions  

## 🌐 Accès depuis un Autre Ordinateur

### URL de Téléchargement
```
https://github.com/[USERNAME]/[REPO]/releases/latest/download/GeneradorReportesSeguridad_v1.0.zip
```

### Pour les Collègues
1. **Partager** le lien du repository GitHub
2. **Naviguer** vers "Releases"
3. **Télécharger** la dernière version
4. **Extraire** et exécuter

---

*Guide créé pour simplifier la distribution d'applications Python via GitHub* 
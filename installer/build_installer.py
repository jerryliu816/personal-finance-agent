#!/usr/bin/env python3
"""
Build script for Personal Finance Agent Windows installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def build_frontend():
    """Build the React frontend"""
    print("Building React frontend...")
    frontend_dir = Path("src/ui/frontend")
    
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Install dependencies
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    # Build frontend
    if not run_command("npm run build", cwd=frontend_dir):
        return False
    
    return True

def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/tray/tray_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/ui/frontend/build', 'src/ui/frontend/build'),
        ('data', 'data'),
        ('config', 'config'),
    ],
    hiddenimports=[
        'uvicorn',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'pystray._win32',
        'PIL._tkinter_finder',
        'sqlalchemy.sql.default_comparator',
        'anthropic',
        'openai',
        'chromadb',
        'sentence_transformers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PersonalFinanceAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    cofile=None,
    icon='installer/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PersonalFinanceAgent',
)
'''
    
    with open('PersonalFinanceAgent.spec', 'w') as f:
        f.write(spec_content)
    
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable with PyInstaller...")
    
    # Create spec file
    if not create_pyinstaller_spec():
        return False
    
    # Run PyInstaller
    if not run_command("pyinstaller PersonalFinanceAgent.spec --clean"):
        return False
    
    return True

def create_inno_setup_script():
    """Create Inno Setup script"""
    script_content = '''
[Setup]
AppName=Personal Finance Agent
AppVersion=1.0.0
AppPublisher=Personal Finance Agent
AppPublisherURL=https://github.com/yourusername/personal-finance-agent
AppSupportURL=https://github.com/yourusername/personal-finance-agent/issues
AppUpdatesURL=https://github.com/yourusername/personal-finance-agent/releases
DefaultDirName={autopf}\\Personal Finance Agent
DefaultGroupName=Personal Finance Agent
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer\\output
OutputBaseFilename=PersonalFinanceAgent-Setup-1.0.0
SetupIconFile=installer\\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startupicon"; Description: "Start automatically with Windows"; GroupDescription: "Startup Options"; Flags: unchecked

[Files]
Source: "dist\\PersonalFinanceAgent\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\Personal Finance Agent"; Filename: "{app}\\PersonalFinanceAgent.exe"
Name: "{group}\\{cm:UninstallProgram,Personal Finance Agent}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Personal Finance Agent"; Filename: "{app}\\PersonalFinanceAgent.exe"; Tasks: desktopicon
Name: "{userappdata}\\Microsoft\\Internet Explorer\\Quick Launch\\Personal Finance Agent"; Filename: "{app}\\PersonalFinanceAgent.exe"; Tasks: quicklaunchicon

[Registry]
Root: HKCU; Subkey: "Software\\Microsoft\\Windows\\CurrentVersion\\Run"; ValueType: string; ValueName: "PersonalFinanceAgent"; ValueData: "{app}\\PersonalFinanceAgent.exe"; Flags: uninsdeletevalue; Tasks: startupicon

[Run]
Filename: "{app}\\PersonalFinanceAgent.exe"; Description: "{cm:LaunchProgram,Personal Finance Agent}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create data directory
    CreateDir(ExpandConstant('{userappdata}\\Personal Finance Agent'));
    CreateDir(ExpandConstant('{userappdata}\\Personal Finance Agent\\data'));
    CreateDir(ExpandConstant('{userappdata}\\Personal Finance Agent\\config'));
  end;
end;
'''
    
    script_path = Path('installer/PersonalFinanceAgent.iss')
    script_path.parent.mkdir(exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    return True

def create_icon():
    """Create a simple icon file"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        size = 256
        image = Image.new('RGB', (size, size), (0, 128, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple dollar sign
        draw.rectangle([(size//4, size//4), (3*size//4, 3*size//4)], fill=(255, 255, 255))
        
        # Save as ICO
        icon_path = Path('installer/icon.ico')
        icon_path.parent.mkdir(exist_ok=True)
        image.save(icon_path, format='ICO', sizes=[(32, 32), (64, 64), (128, 128), (256, 256)])
        
        return True
    except ImportError:
        print("PIL not available, skipping icon creation")
        return True
    except Exception as e:
        print(f"Error creating icon: {e}")
        return True

def create_license():
    """Create a simple LICENSE file"""
    license_content = '''MIT License

Copyright (c) 2024 Personal Finance Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    
    return True

def main():
    """Main build process"""
    print("Starting Personal Finance Agent build process...")
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("This build script is designed for Windows. Skipping installer creation.")
        return True
    
    steps = [
        ("Creating icon", create_icon),
        ("Creating license", create_license),
        ("Building frontend", build_frontend),
        ("Building executable", build_executable),
        ("Creating Inno Setup script", create_inno_setup_script),
    ]
    
    for step_name, step_func in steps:
        print(f"\n=== {step_name} ===")
        if not step_func():
            print(f"Failed at step: {step_name}")
            return False
        print(f"✓ {step_name} completed successfully")
    
    print("\n=== Build completed successfully! ===")
    print("To create the installer:")
    print("1. Install Inno Setup (https://jrsoftware.org/isinfo.php)")
    print("2. Open installer/PersonalFinanceAgent.iss in Inno Setup")
    print("3. Click 'Compile' to create the installer")
    print("\nOr run: iscc installer/PersonalFinanceAgent.iss")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
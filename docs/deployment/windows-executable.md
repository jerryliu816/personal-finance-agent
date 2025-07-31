# Windows Executable Generation Guide

Step-by-step guide to generate a Windows executable for the Personal Finance Agent.

## Prerequisites

### System Requirements
- **Windows 10/11** (64-bit)
- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Git** for source control

### Required Tools
- **PyInstaller** for executable creation
- **Inno Setup** (optional, for installer creation)

## Quick Start

Run the automated build script:

```bash
python installer/build_installer.py
```

This handles the entire process automatically.

## Manual Step-by-Step Process

### Step 1: Environment Setup

```bash
# Clone repository
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Build Frontend

```bash
cd src/ui/frontend

# Install Node dependencies
npm install

# Build production frontend
npm run build

# Return to project root
cd ../../..
```

### Step 3: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 4: Generate Executable

#### Option A: Using Existing Build Script
```bash
python installer/build_installer.py
```

#### Option B: Manual PyInstaller
```bash
# Create spec file (if not exists)
pyi-makespec --onedir --windowed --icon=installer/icon.ico src/tray/tray_app.py

# Build executable
pyinstaller PersonalFinanceAgent.spec --clean
```

### Step 5: Test Executable

```bash
# Test the generated executable
dist\PersonalFinanceAgent\PersonalFinanceAgent.exe
```

## PyInstaller Configuration

The build uses a spec file (`PersonalFinanceAgent.spec`) with these key configurations:

### Entry Point
- Main script: `src/tray/tray_app.py`
- Creates a windowed application (no console)

### Included Data Files
- Frontend build: `src/ui/frontend/build`
- Data directory: `data`
- Configuration: `config`

### Hidden Imports
Critical modules that PyInstaller might miss:
- `uvicorn` and related modules
- `pystray._win32`
- `PIL._tkinter_finder`
- `sqlalchemy.sql.default_comparator`
- AI libraries: `anthropic`, `openai`, `chromadb`, `sentence_transformers`

## Creating Windows Installer (Optional)

### Prerequisites
1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)

### Generate Installer
```bash
# Using the build script (includes installer generation)
python installer/build_installer.py

# Or manually compile the Inno Setup script
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\PersonalFinanceAgent.iss
```

The installer will be created in `installer/output/PersonalFinanceAgent-Setup-1.0.0.exe`

## Output Files

After successful build:

```
dist/
└── PersonalFinanceAgent/
    ├── PersonalFinanceAgent.exe    # Main executable
    ├── _internal/                  # Dependencies and libraries
    ├── src/                       # Application source
    └── data/                      # Data files
```

Installer (if created):
```
installer/
└── output/
    └── PersonalFinanceAgent-Setup-1.0.0.exe
```

## Troubleshooting

### Missing Module Errors
If the executable fails with "ModuleNotFoundError":
1. Add the missing module to `hiddenimports` in the spec file
2. Rebuild with `pyinstaller PersonalFinanceAgent.spec --clean`

### File Not Found Errors
If data files are missing:
1. Verify the `datas` section in the spec file includes all necessary directories
2. Check that paths are correct relative to the project root

### Large Executable Size
To reduce size:
1. Add unused modules to `excludes` in the spec file
2. Enable UPX compression (already enabled by default)
3. Remove unnecessary data files

### Frontend Build Issues
```bash
# If Node memory issues occur
set NODE_OPTIONS=--max_old_space_size=4096
cd src/ui/frontend
npm run build
```

## Build Script Details

The `installer/build_installer.py` script performs these steps:

1. **Frontend Build**: Compiles React application
2. **Icon Creation**: Generates application icon (if PIL available)
3. **License Creation**: Creates MIT license file
4. **Executable Build**: Uses PyInstaller with predefined spec
5. **Installer Generation**: Creates Inno Setup script and compiles installer

## Verification

Test the executable on a clean Windows system:

1. Copy `dist/PersonalFinanceAgent/` to target system
2. Run `PersonalFinanceAgent.exe`
3. Verify all features work correctly
4. Check system tray integration

## Distribution

### Standalone Executable
Distribute the entire `dist/PersonalFinanceAgent/` directory as a ZIP file.

### Windows Installer
Distribute the generated `.exe` installer from `installer/output/`.

The installer provides:
- Automatic installation to Program Files
- Start Menu shortcuts
- Optional desktop shortcut
- Optional startup with Windows
- Uninstaller registration

## Notes

- The executable includes all dependencies and can run on systems without Python installed
- First startup may be slower as the application initializes
- The application requires internet connectivity for AI features
- User data is stored in `%APPDATA%\Personal Finance Agent\`
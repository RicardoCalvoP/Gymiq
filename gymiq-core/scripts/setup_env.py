import os
import sys
import subprocess
from pathlib import Path

# scripts/setup_env.py -> ROOT_DIR = carpeta raíz del proyecto (gymiq-core)
ROOT_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT_DIR / "venv"


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    print(f"Project root: {ROOT_DIR}")

    # 1. Crear venv si no existe
    if not VENV_DIR.exists():
        run([python_exe, "-m", "venv", str(VENV_DIR)])
        print(f"Virtual environment 'venv' created at: {VENV_DIR}")
    else:
        print(f"Virtual environment 'venv' already exists at: {VENV_DIR}")

    # 2. Instalar dependencias en el venv
    if os.name == "nt":  # Windows
        venv_python = VENV_DIR / "Scripts" / "python.exe"
    else:  # Linux / macOS
        venv_python = VENV_DIR / "bin" / "python"

    if not venv_python.exists():
        print(f"Could not find venv python at {venv_python}")
        sys.exit(1)

    print(f"Using venv Python: {venv_python}")

    requirements_path = ROOT_DIR / "requirements.txt"
    if not requirements_path.exists():
        print(f"Could not find requirements.txt at {requirements_path}")
        sys.exit(1)

    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(venv_python), "-m", "pip", "install", "-r", str(requirements_path)])

    print("Environment setup completed.")
    print()
    print("To activate the virtual environment:")
    if os.name == "nt":
        print(r"  .\venv\Scripts\Activate.ps1   (PowerShell, from gymiq-core)")
        print(r"  venv\Scripts\activate.bat     (CMD, from gymiq-core)")
    else:
        print("  source venv/bin/activate")


if __name__ == "__main__":
    main()

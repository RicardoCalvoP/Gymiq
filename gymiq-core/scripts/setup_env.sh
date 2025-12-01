#!/usr/bin/env bash

if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Python no encontrado. Instálalo y asegúrate de que esté en PATH."
    exit 1
fi

echo "Usando Python: $PYTHON_CMD"

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "Virtual environment 'venv' creado."
else
    echo "Virtual environment 'venv' ya existe."
fi

if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "No se encontró el archivo de activación del venv."
    exit 1
fi

echo "Entorno activado."

$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

echo "Setup completo."

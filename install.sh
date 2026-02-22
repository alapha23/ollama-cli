#!/bin/bash

# Ollama CLI Installer
# Installs Ollama CLI, Ollama, and ComfyUI

set -e

echo "==========================================="
echo "      Ollama CLI All-in-One Installer      "
echo "==========================================="
echo ""

# 1. Check Prerequisites
echo "[*] Checking system..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Error: git is required but not found."
    exit 1
fi

# 2. Install Ollama CLI
echo ""
echo "[*] Installing Ollama CLI..."
# Ensure we are in the directory containing pyproject.toml
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

if [ -f "pyproject.toml" ]; then
    pip3 install .
    echo "✅ Ollama CLI installed."
else
    echo "Error: Could not find pyproject.toml. Make sure you run this script from the ollama-cli directory."
    exit 1
fi

# 3. Install Ollama (Optional)
echo ""
echo "-------------------------------------------"
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed."
else
    read -p "Do you want to install Ollama (LLM Server)? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "[*] Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        echo "✅ Ollama installed."
    else
        echo "Skipping Ollama installation."
    fi
fi

# 4. Install ComfyUI (Optional)
echo ""
echo "-------------------------------------------"
read -p "Do you want to install ComfyUI (Image Generation)? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    INSTALL_DIR="$HOME/ComfyUI"
    if [ -d "$INSTALL_DIR" ]; then
        echo "⚠️  ComfyUI directory already exists at $INSTALL_DIR"
        read -p "Update existing installation? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$INSTALL_DIR"
            git pull
            pip3 install -r requirements.txt
            echo "✅ ComfyUI updated."
        fi
    else
        echo "[*] Cloning ComfyUI to $INSTALL_DIR..."
        git clone https://github.com/comfyanonymous/ComfyUI.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
        echo "[*] Installing ComfyUI dependencies..."
        pip3 install -r requirements.txt
        echo "✅ ComfyUI installed."
        
        # 5. Download Image Generation Model
        echo ""
        echo "[*] Downloading Image Generation Model (DreamShaper 8)..."
        MODEL_DIR="models/checkpoints"
        mkdir -p "$MODEL_DIR"
        MODEL_PATH="$MODEL_DIR/dreamshaper_8.safetensors"
        if [ ! -f "$MODEL_PATH" ]; then
            echo "    This may take a few minutes (approx. 2GB)..."
            curl -L "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_8_pruned.safetensors" -o "$MODEL_PATH"
            echo "✅ Model downloaded."
        else
            echo "✅ Model already exists."
        fi

        echo ""
        echo "[!] To use Image Generation, you must start ComfyUI:"
        echo "    cd $INSTALL_DIR"
        echo "    python3 main.py"
    fi
    
    # Update config to point to ComfyUI
    # We use a python one-liner to update the json config safely
    python3 -c "
import json
import os
config_path = os.path.expanduser('~/.ollama-cli-config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {}
config['comfy_url'] = 'http://127.0.0.1:8188'
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('✅ Configured ollama-cli to use ComfyUI at http://127.0.0.1:8188')
"
else
    echo "Skipping ComfyUI installation."
fi

echo ""
echo "==========================================="
echo "      Installation Complete! 🚀            "
echo "==========================================="
echo ""
echo "To start the CLI, run:"
echo "  ollama-cli"
echo ""
if command -v ollama &> /dev/null; then
    echo "Ensure Ollama is running:"
    echo "  ollama serve"
fi
echo ""

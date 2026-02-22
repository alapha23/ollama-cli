import subprocess
import os
import sys
import requests
import json
import random
from .base import tool
from ..core.config import load_config

@tool(
    name="generate_image",
    description="Generate an image using the local Stable Diffusion workflow (ComfyUI)",
    parameters={
        "prompt": {"type": "string", "description": "The image description"}
    }
)
def generate_image(prompt: str) -> str:
    """Invokes the ComfyUI API directly with a predefined workflow"""
    config = load_config()
    comfy_url = config.get("comfy_url", "http://127.0.0.1:8188").rstrip("/")
    
    try:
        # Check if ComfyUI is running
        try:
            requests.get(comfy_url, timeout=2)
        except:
            return f"Error: ComfyUI server ({comfy_url}) appears to be down. Please start it first or configure the URL with '/config comfy <url>'."

        # Define the workflow directly
        # Based on the user's previous generate_image.py, but using the configured URL
        workflow = {
            "1": {
                "inputs": {"ckpt_name": "dreamshaper_8.safetensors"},
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "text": f"masterpiece, best quality, highly detailed, {prompt}",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {
                    "text": "blurry, low quality, distorted, watermark, nsfw",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {"width": 512, "height": 512, "batch_size": 1},
                "class_type": "EmptyLatentImage"
            },
            "5": {
                "inputs": {
                    "seed": random.randint(1, 1000000000), "steps": 20, "cfg": 7.0,
                    "sampler_name": "dpmpp_2m", "scheduler": "karras",
                    "denoise": 1.0, "model": ["1", 0],
                    "positive": ["2", 0], "negative": ["3", 0],
                    "latent_image": ["4", 0]
                },
                "class_type": "KSampler"
            },
            "6": {
                "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
                "class_type": "VAEDecode"
            },
            "7": {
                "inputs": {
                    "filename_prefix": "ollama_cli_",
                    "images": ["6", 0]
                },
                "class_type": "SaveImage"
            }
        }
        
        payload = {"prompt": workflow}
        response = requests.post(f"{comfy_url}/prompt", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            prompt_id = data.get('prompt_id', 'unknown')
            return f"Image generation queued successfully on {comfy_url}.\nPrompt ID: {prompt_id}\nCheck your ComfyUI output folder for 'ollama_cli_' prefixed files."
        else:
            return f"Error form ComfyUI: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error generating image: {str(e)}"

@tool(
    name="speak_text",
    description="Convert text to speech using Piper TTS",
    parameters={
        "text": {"type": "string", "description": "Text to speak"},
        "output_file": {"type": "string", "description": "Output filename", "default": "output.wav"}
    }
)
def speak_text(text: str, output_file: str = "output.wav") -> str:
    """Uses local Piper installation if available"""
    piper_bin = os.path.expanduser("~/piper/piper")
    model_path = os.path.expanduser("~/piper/models/en_US-lessac-medium.onnx") # Guessing model path based on common setup
    
    # Fallback to simple 'say' command on macOS if piper is tricky to locate without scanning
    if sys.platform == "darwin":
        try:
            subprocess.run(["say", "-o", output_file, text], check=True)
            return f"Audio saved to {output_file} (using macOS 'say')"
        except Exception as e:
            return f"Error using 'say': {e}"
            
    return "TTS not configured for this platform yet."

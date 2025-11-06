import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the Gradio interface
from src.app.app import iface

if __name__ == "__main__":
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)

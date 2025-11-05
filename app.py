from src.app.app import create_interface

# Expose iface for Hugging Face Spaces, and allow local run
iface = create_interface()

if __name__ == "__main__":
    iface.launch()

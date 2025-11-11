import gradio as gr
from src.app.inference import load_model, predict
import time
from pathlib import Path
from PIL import Image
import numpy as np

# Load models at startup
models = {}
model_paths = {
    "YOLOv8": "models/yolov8_best.pt",
    "YOLOv12": "models/yolov12_best.pt"
}

# Load available models
for name, path in model_paths.items():
    if Path(path).exists():
        models[name] = load_model(path)
        print(f"✓ Loaded {name}")
    else:
        print(f"✗ {name} not found at {path}")

# Load test images
test_images_dir = Path("data/processed/test/images")
test_images = []
if test_images_dir.exists():
    test_images = sorted(list(test_images_dir.glob("*.png")) + 
                        list(test_images_dir.glob("*.jpg")) + 
                        list(test_images_dir.glob("*.jpeg")))
    print(f"✓ Found {len(test_images)} test images")
else:
    print("✗ Test images not found")

def detect_cavities(image, model_name):
    """Detect cavities using selected model"""
    if model_name not in models:
        return None, f"Error: {model_name} not loaded"
    
    start = time.time()
    result_img, boxes = predict(models[model_name], image)
    inference_time = time.time() - start
    
    summary = f"Model: {model_name}\nDetected: {len(boxes)} cavities\nTime: {inference_time:.3f}s"
    return result_img, summary

def compare_models(image):
    """Compare both models side-by-side"""
    if len(models) < 2:
        return None, None, "Need both models to compare"
    
    results = {}
    for name in models.keys():
        start = time.time()
        result_img, boxes = predict(models[name], image)
        results[name] = {
            'image': result_img,
            'boxes': len(boxes),
            'time': time.time() - start
        }
    
    # Create comparison summary
    summary = "Model Comparison:\n"
    for name, data in results.items():
        summary += f"\n{name}:\n  Detections: {data['boxes']}\n  Time: {data['time']:.3f}s"
    
    model_names = list(results.keys())
    img1 = results[model_names[0]]['image'] if len(model_names) > 0 else None
    img2 = results[model_names[1]]['image'] if len(model_names) > 1 else None
    
    return img1, img2, summary

# Create interface with tabs
with gr.Blocks(title="Dental Cavity Detection") as iface:
    gr.Markdown("#Dental X-ray Cavity Detection")
    gr.Markdown("Upload a dental X-ray to detect cavities using YOLO models")
    
    with gr.Tab("Single Model"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Upload or Select from Test Set")
                input_img = gr.Image(type="numpy", label="Upload X-ray")
                
                if test_images:
                    gr.Markdown("**Or select from test images:**")
                    test_gallery = gr.Gallery(
                        value=[(str(img), img.stem) for img in test_images[:12]],  # Show first 12
                        label="Test Images",
                        columns=4,
                        height="auto"
                    )
                
                model_choice = gr.Dropdown(
                    choices=list(models.keys()),
                    value=list(models.keys())[0] if models else None,
                    label="Select Model"
                )
                btn_detect = gr.Button("Detect Cavities", variant="primary")
            
            with gr.Column():
                output_img = gr.Image(label="Detection Result")
                output_text = gr.Textbox(label="Summary", lines=4)
        
        # Function to load selected test image
        def load_test_image(evt: gr.SelectData):
            img_path = test_images[evt.index]
            img = Image.open(img_path)
            return np.array(img)
        
        if test_images:
            test_gallery.select(
                fn=load_test_image,
                outputs=[input_img]
            )
        
        btn_detect.click(
            fn=detect_cavities,
            inputs=[input_img, model_choice],
            outputs=[output_img, output_text]
        )
    
    with gr.Tab("Compare Models"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Upload or Select from Test Set")
                compare_input = gr.Image(type="numpy", label="Upload X-ray")
                
                if test_images:
                    gr.Markdown("**Or select from test images:**")
                    compare_gallery = gr.Gallery(
                        value=[(str(img), img.stem) for img in test_images[:12]],
                        label="Test Images",
                        columns=4,
                        height="auto"
                    )
                
                btn_compare = gr.Button("Compare Models", variant="primary")
            
            with gr.Column():
                compare_out1 = gr.Image(label=list(models.keys())[0] if len(models) > 0 else "Model 1")
                compare_out2 = gr.Image(label=list(models.keys())[1] if len(models) > 1 else "Model 2")
                compare_text = gr.Textbox(label="Comparison Summary", lines=6)
        
        # Load test image for comparison
        def load_compare_image(evt: gr.SelectData):
            img_path = test_images[evt.index]
            img = Image.open(img_path)
            return np.array(img)
        
        if test_images:
            compare_gallery.select(
                fn=load_compare_image,
                outputs=[compare_input]
            )
        
        btn_compare.click(
            fn=compare_models,
            inputs=[compare_input],
            outputs=[compare_out1, compare_out2, compare_text]
        )

if __name__ == "__main__":
    iface.launch()

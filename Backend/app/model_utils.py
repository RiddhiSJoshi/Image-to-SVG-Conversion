# create a backend API that uses AI (StarVector model from Hugging Face) to automatically convert raster images (like PNG or JPEG) into SVG vector graphics.
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch
import io

# Load StarVector model and processor (once)
processor = AutoProcessor.from_pretrained("facebook/starvector")
model = AutoModelForVision2Seq.from_pretrained("facebook/starvector")

def image_to_svg(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=1024)

        svg = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        return svg
    except Exception as e:
        raise RuntimeError(f"SVG conversion failed: {e}")

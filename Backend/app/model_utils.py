# model_utils.py

from PIL import Image
import torch
import io, os, hashlib
from transformers import AutoModelForCausalLM

# Load once at module level to avoid reloading for every call
model_name = "starvector/starvector-8b-im2svg"
starvector = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    trust_remote_code=True
)
processor = starvector.model.processor
tokenizer = starvector.model.svg_transformer.tokenizer

starvector.cuda()
starvector.eval()

# Add this global dictionary
cache = {}

def get_image_hash(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()

def image_to_svg(image_bytes: bytes) -> str:
    image_hash = get_image_hash(image_bytes)

    #  Check cache
    if image_hash in cache:
        print("Using cached SVG")
        return cache[image_hash]
    # Convert image bytes to PIL image
    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Preprocess image
    image = processor(image_pil, return_tensors="pt")['pixel_values'].cuda()
    if not image.shape[0] == 1:
        image = image.squeeze(0)
    
    batch = {"image": image}

    # Generate SVG
    raw_svg = starvector.generate_im2svg(batch, max_length=4000)[0]

    # Save to disk
    os.makedirs("output_svgs", exist_ok=True)
    filename = f"output_svgs/{image_hash}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_svg)

    # Save to cache
    cache[image_hash] = raw_svg

    return raw_svg

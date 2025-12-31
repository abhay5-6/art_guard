from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os
import re

# Offline mode (as you already had)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

# --------------------------------------------------
# Load model ONCE (critical for performance)
# --------------------------------------------------
_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    use_fast=True,
    local_files_only=True,
)
_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    local_files_only=True,
)
_model.eval()


# --------------------------------------------------
# Caption generation
# --------------------------------------------------
def caption_image(image_path):
    """
    Takes an image path and returns a raw BLIP caption string.
    """
    image = Image.open(image_path).convert("RGB")

    inputs = _processor(image, return_tensors="pt")

    with torch.no_grad():
        output = _model.generate(
            **inputs,
            max_new_tokens=30,
        )

    caption = _processor.decode(
        output[0],
        skip_special_tokens=True,
    )

    return caption.lower()


# --------------------------------------------------
# Public API (DO NOT change signature)
# --------------------------------------------------
def generate_base_name(image_path):
    """
    MAIN PUBLIC FUNCTION.

    Generates a base name directly from BLIP caption.
    - Full caption
    - Word order preserved
    - Filesystem-safe
    - No artificial limits
    """
    caption = caption_image(image_path)

    # Keep only letters, numbers, and spaces
    caption = re.sub(r"[^a-zA-Z0-9\s]", "", caption)

    # Normalize whitespace
    caption = re.sub(r"\s+", " ", caption).strip()

    if not caption:
        return "UNTITLED"

    # Convert to filesystem-safe name
    return "_".join(word.upper() for word in caption.split())

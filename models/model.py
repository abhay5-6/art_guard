from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"


# Load once (important for performance)
_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base",
     use_fast=True
)
_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
_model.eval()

IMPORTANT_WORDS = {
    "girl", "boy", "man", "woman",
    "apple", "tree", "house",
    "shadow", "road", "sky",
    "field", "cloud", "sun"
}


def caption_image(image_path):
    """
    Takes an image path and returns a raw caption string.
    """
    image = Image.open(image_path).convert("RGB")

    inputs = _processor(image, return_tensors="pt")

    with torch.no_grad():
        output = _model.generate(
            **inputs,
            max_new_tokens=20
        )

    caption = _processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption.lower()


def extract_semantic_tokens(caption):
    """
    Extracts important semantic words from caption.
    """
    words = caption.replace(",", "").split()
    return [w for w in words if w in IMPORTANT_WORDS]


def generate_base_name(image_path):
    """
    MAIN PUBLIC FUNCTION.

    Returns a base semantic name string like:
    'APPLE_GIRL' or 'ROAD_SKY'
    """
    caption = caption_image(image_path)
    tokens = extract_semantic_tokens(caption)

    if not tokens:
        return "UNTITLED"

    # keep only first 2 meaningful tokens
    tokens = tokens[:2]

    return "_".join(t.upper() for t in tokens)

# Defines the two AI models from Hugging Face integrated into the GUI

import os
import torch
from utils import timing, cached_result, simple_logger
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)
from diffusers import StableDiffusionPipeline


# Base model interface
class ModelInterface:
    def load(self):
        raise NotImplementedError

    def run(self, input_data):
        raise NotImplementedError

    def info(self):
        raise NotImplementedError


# Defines function for log messages, etc.
class LoggerMixin:
    def log(self, message):
        simple_logger(message)


# Text-to-Image AI Model - Stable Diffusion
class TextToImageModel(ModelInterface, LoggerMixin):
    def __init__(self):
        self._model = None
        self._loaded = False

    @timing
    def load(self):
        if self._loaded:
            self.log("Stable Diffusion already loaded.")
            return
        try:
            self._model = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            if torch.cuda.is_available():
                self._model = self._model.to("cuda")

            # Optional: enable xformers for faster attention
            try:
                self._model.enable_xformers_memory_efficient_attention()
            except Exception:
                self.log("xFormers not available, skipping optimization.")

            self._loaded = True
            self.log("Stable Diffusion (base) loaded successfully.")
        except Exception as e:
            raise RuntimeError("Failed to load text-to-image model. " + str(e))

    @cached_result
    @timing
    def run(self, prompt: str):
        if not self._loaded:
            self.load()

        out_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(out_dir, exist_ok=True)
        result = self._model(
            prompt,
            num_inference_steps=15,  # faster than default 50
            guidance_scale=7.0,
            height=384,
            width=384
        )
        image = result.images[0]

        import uuid
        filename = os.path.join(out_dir, f"t2i_result_{uuid.uuid4().hex[:8]}.png")
        image.save(filename)

        return {"status": "ok", "path": filename, "prompt": prompt}

    def info(self):
        return {
            "name": "Stable Diffusion v1.5",
            "type": "text-to-image",
            "description": "Generates images from text prompts."
        }


# Image-to-Text AI Model - BLIP
class BlipCaptionModel(ModelInterface, LoggerMixin):
    def __init__(self):
        self._model = None
        self._processor = None
        self._loaded = False

    @timing
    def load(self):
        if self._loaded:
            self.log("BLIP already loaded.")
            return
        try:
            self._processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-large"
            )
            self._model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-large"
            )
            if torch.cuda.is_available():
                self._model = self._model.to("cuda")
            self._loaded = True
            self.log("BLIP captioning model loaded.")
        except Exception as e:
            raise RuntimeError("Failed to load BLIP model. " + str(e))

    @cached_result
    @timing
    def run(self, image_path: str):
        if not self._loaded:
            self.load()

        from PIL import Image
        raw_image = Image.open(image_path).convert("RGB")

        inputs = self._processor(raw_image, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        out = self._model.generate(**inputs, max_length=40)
        caption = self._processor.decode(out[0], skip_special_tokens=True)

        return {"status": "ok", "caption": caption, "path": image_path}

    def info(self):
        return {
            "name": "Salesforce/blip-image-captioning-large",
            "type": "image-to-text",
            "description": "BLIP captioning model that generates natural language captions for images."
        }


# Model Manager (Polymorphism)
class ModelManager:
    def __init__(self):
        self.models = {
            "Text-to-Image": TextToImageModel(),
            "Image-to-Text": BlipCaptionModel()
        }

    def get_model(self, key):
        return self.models.get(key)

    def available_models(self):
        return list(self.models.keys())

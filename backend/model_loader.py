# backend/model_loader.py
import torch
from diffusers import StableDiffusion3Pipeline, BitsAndBytesConfig, SD3Transformer2DModel

def load_model():
    model_id = "stabilityai/stable-diffusion-3.5-large"

    # Define 4-bit quantization config
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # Load only the transformer in quantized format
    model_nf4 = SD3Transformer2DModel.from_pretrained(
        model_id,
        subfolder="transformer",
        quantization_config=nf4_config,
        torch_dtype=torch.bfloat16
    )

    # Load the full pipeline with injected transformer
    pipe = StableDiffusion3Pipeline.from_pretrained(
        model_id,
        transformer=model_nf4,
        torch_dtype=torch.bfloat16
    )

    # Enable model CPU offloading to avoid CUDA OOM
    pipe.enable_model_cpu_offload()

    return pipe
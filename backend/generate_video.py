# backend/generate_video.py

import base64
from io import BytesIO
from PIL import Image
import torch
from diffusers import DiffusionPipeline

video_pipe = None

def load_video_model():
    global video_pipe
    if video_pipe is None:
        video_pipe = DiffusionPipeline.from_pretrained(
            "Lightricks/LTX-VideoQ8", 
            torch_dtype=torch.float16,
            variant="fp16",
            low_cpu_mem_usage=True
        ).to("cuda" if torch.cuda.is_available() else "cpu")

        video_pipe.enable_model_cpu_offload()

        try:
            video_pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            pass

    return video_pipe

def generate_video_from_image(base64_image: str) -> str:

    img_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(img_data)).convert("RGB")

    image = image.resize((768, 512), resample=Image.LANCZOS)

    pipe = load_video_model()
    result = pipe(
        image=image,
        num_frames=12,              
        guidance_scale=5.0,          
        decode_chunk_size=2          
    )

    frames = result.frames

    import imageio
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        imageio.mimsave(tmp.name, frames, fps=7, quality=8)
        tmp.seek(0)
        mp4_bytes = tmp.read()

    return base64.b64encode(mp4_bytes).decode("utf-8")

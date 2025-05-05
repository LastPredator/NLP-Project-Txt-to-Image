# backend/generate.py
from io import BytesIO
import base64

def generate_image(model, prompt, steps=28, guidance=4.5, width=512, height=512):
    image = model(
        prompt=prompt,
        num_inference_steps=steps,
        guidance_scale=guidance,
        width=width,
        height=height
    ).images[0]

    buf = BytesIO()
    image.save(buf, format="PNG")
    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    return img_str
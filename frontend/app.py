import streamlit as st
from grpc_client import get_image
from PIL import Image
import io
import base64
import random
from deep_translator import GoogleTranslator
from diffusers import StableVideoDiffusionPipeline
import tempfile
import torch

# --- UI Setup ---
st.set_page_config(page_title="AI Image Generator", layout="wide", page_icon="🎨")

# --- Custom Styling ---
bg_color = "#0f0f0f"
text_color = "white"
st.markdown(f"""
    <style>
        .main {{ background-color: {bg_color}; color: {text_color}; }}
        .stButton > button {{
            border-radius: 12px;
            padding: 0.5rem 1rem;
            background-color: #ff4b4b;
            color: white;
            border: none;
        }}
        .image-wrapper {{
            position: relative;
            text-align: center;
            margin-bottom: 20px;
        }}
        .image-wrapper img {{
            width: 100%;
            border-radius: 10px;
        }}
        .download-btn {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: rgba(0,0,0,0.6);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 10px;
            text-decoration: none;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .image-wrapper:hover .download-btn {{
            opacity: 1;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = []
if "selected_image_b64" not in st.session_state:
    st.session_state["selected_image_b64"] = None

# --- Title and Info ---
st.title("✨ AI Text-to-Image Generator")
st.markdown("Generate unique visuals from text prompts using **Stable Diffusion 3.5**, and turn any image into a video using **Stable Video Diffusion XT** 🧠🎥")
st.caption("🌍 You can write prompts in any language. We’ll automatically translate them to English.")

# --- Prompt Inputs ---
col1, col2 = st.columns(2)
with col1:
    prompt = st.text_area("📝 Main Prompt", "A cute kitten", height=120)
with col2:
    context = st.text_area("🔍 Optional Context", "Sitting on paws on a sofa", height=120)

# --- Variations and Resolution ---
num_variations = st.selectbox("🔄 Number of Variations", [1, 2, 3, 4, 5], index=0)
resolution_map = {
    "256 x 256": (256, 256),
    "512 x 512": (512, 512),
    "768 x 768": (768, 768),
    "1024 x 1024": (1024, 1024),
}
resolution_choice = st.selectbox("🖼️ Image Resolution", list(resolution_map.keys()), index=1)
width, height = resolution_map[resolution_choice]

# --- Generate Button ---
if st.button("🎨 Generate Variations"):
    st.session_state["generated_images"] = []
    st.session_state["selected_image_b64"] = None

    with st.spinner("Translating prompts and generating images..."):
        try:
            translated_prompt = GoogleTranslator(source='auto', target='en').translate(prompt)
            translated_context = GoogleTranslator(source='auto', target='en').translate(context)
        except Exception as e:
            st.error(f"❌ Translation error: {e}")
            st.stop()

        for i in range(num_variations):
            variation_prompt = f"{translated_prompt} [{random.randint(1000,9999)}]"
            img_bytes, err = get_image(variation_prompt, translated_context, width, height)

            if img_bytes:
                image = Image.open(io.BytesIO(img_bytes))
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                b64_img = base64.b64encode(buffered.getvalue()).decode()
                st.session_state["generated_images"].append(b64_img)
            else:
                st.error(f"❌ Error in variation {i+1}: {err}")

# --- Display Generated Images and Selection Buttons ---
if st.session_state["generated_images"]:
    cols = st.columns(len(st.session_state["generated_images"]))
    for i, b64_img in enumerate(st.session_state["generated_images"]):
        with cols[i]:
            img_html = f"""
            <div class="image-wrapper">
                <img src="data:image/png;base64,{b64_img}" alt="Variation {i+1}" />
                <a class="download-btn" href="data:image/png;base64,{b64_img}" download="variation_{i+1}.png">⬇ Download</a>
            </div>
            """
            st.markdown(img_html, unsafe_allow_html=True)

            if st.button(f"🎯 Select Variation {i+1} for Video", key=f"select_{i}"):
                st.session_state["selected_image_b64"] = b64_img
                st.success(f"✅ Selected Variation {i+1} for video")

# --- Convert to Video Section ---
st.subheader("🎬 Convert Selected Image to Video")
if st.session_state["selected_image_b64"]:
    st.info("🎥 Generating video... please wait.")

    with st.spinner("Running Stable Video Diffusion..."):
        try:
            # Load selected image
            img_bytes = base64.b64decode(st.session_state["selected_image_b64"])
            input_image = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((1024, 576))

            # Load the pipeline from Hugging Face
            pipe = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid",
                torch_dtype=torch.float16,
                variant="fp16"
            ).to("cuda")

            frames = pipe(input_image, decode_chunk_size=16).frames[0]  # (F, H, W, C)

            import imageio
            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            imageio.mimwrite(temp_video_file.name, frames, fps=7, quality=8)

            st.video(temp_video_file.name)

            with open(temp_video_file.name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:video/mp4;base64,{b64}" download="generated_video.mp4">⬇ Download Video</a>'
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Failed to generate video: {e}")
else:
    st.warning("⚠️ Please select an image to generate a video.")
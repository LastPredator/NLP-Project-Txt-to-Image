# End of Semester Project - AI Image & Video Generation System

This project demonstrates an end-to-end system for generating both images and videos using text prompts. It uses gRPC for communication between frontend and backend, and supports real-time interaction through a web interface made with Streamlit.

The core of the system relies on state-of-the-art models:
- **Stable Diffusion 3.5 (Large)** for image generation
- **Stable Video Diffusion** for generating short videos

---

## 📁 Project Structure

```
NLP/
├── backend/
│   ├── generate.py           # Handles image/video generation from prompt
│   ├── generate_video.py     # Specific to video generation
│   ├── main.py               # Starts the gRPC server
│   └── requirements.txt      # Backend dependencies
│
├── frontend/
│   ├── app.py                # Streamlit frontend
│   ├── grpc_client.py        # Connects frontend to backend over gRPC
│   ├── image_gen.proto       # Protocol Buffers file defining the service
│   └── requirements.txt      # Frontend dependencies
│
├── docker-compose.yml       # Docker setup for both services
└── README.md                 # You're here
```

---

## 🔧 Setup Instructions

### 🐳 Run With Docker
```bash
docker-compose up --build
```
- **Frontend (Streamlit)** will be available at: http://localhost:8501
- **Backend (gRPC Server)** runs on: localhost:50051

This is the easiest way to test the full system.

### 🐍 Run Without Docker (For Development)
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Testing With Postman

If you want to test the gRPC service directly:
1. Open the **Postman gRPC client**
2. Upload the `image_gen.proto` file
3. Call the method: `GenerateImage`
4. Use message like:
```json
{
  "prompt": "a cat flying through space on a rocket"
}
```
5. You’ll receive the `image_data` (base64 PNG)

---

## 🧠 Architecture

```
[User Input (Text)]
     ↓
[Frontend - Streamlit]
     ↓
[gRPC Call to Backend]
     ↓
[Image/Video Generation using Stable Diffusion 3.5 or SVD]
     ↓
[Base64 Result Returned to Frontend]
     ↓
[Image/Video Displayed to User]
```

---

## 📚 Model Details

- **Stable Diffusion 3.5 (Large)** used via HuggingFace Diffusers for high-quality text-to-image.
- **Stable Video Diffusion** is used optionally for video clips. This was integrated via `generate_video.py`.
- Both models run with PyTorch.

---

## ❌ Limitations

- **No GPU support in Docker** by default
- **Cold start is slow** due to model loading
- **Not secured for production**, no auth layer
- **gRPC message limit** can break large image/video transfers

---

## 📬 Notes To Instructor

I’ve tried to keep the code clean and modular. The `backend` is separated for inference so it could be scaled independently later. The `frontend` uses Streamlit to reduce overhead and quickly show results in a usable UI.

Everything is containerized for portability, and tested using both manual calls (Postman) and UI interface.


---

**Submitted by:** _22i-0561 Hassan Ali Shoro, 22i-0585 Ibaad Ahmed Chaudry, 22i-2142 Abdullah Kaif_
**Course:** End of Semester NLP Project
**Tools:** Python, Docker, gRPC, HuggingFace, Streamlit, Postman

import sys
import os

# Create a reference to the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from PIL import Image
from model import load_model, denoise_pil_image

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model globally (cold start optimization)
try:
    print("Loading model...")
    model = load_model()
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/api/denoise")
async def denoise_image_endpoint(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read image
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        # Denoise
        denoised_image = denoise_pil_image(image, model)

        # Save to buffer
        buf = BytesIO()
        denoised_image.save(buf, format="PNG")
        buf.seek(0)
        
        # Return bytes
        from fastapi.responses import Response
        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        print(f"Error during processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# For local development (when running uvicorn api.index:app)
# This will serve files from the 'public' directory at the root URL
# In Vercel, vercel.json handles this.
if os.path.exists(os.path.join(parent_dir, "public")):
    app.mount("/", StaticFiles(directory=os.path.join(parent_dir, "public"), html=True), name="public")

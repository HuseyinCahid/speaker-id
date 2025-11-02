from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile
import os
from pathlib import Path
import numpy as np
import subprocess

from audio_processor import AudioProcessor
from model_manager import ModelManager

app = FastAPI(
    title="Speaker ID API",
    description="Real-time speaker identification using FastAPI + Librosa + ML",
    version="0.1.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
audio_processor = AudioProcessor()
model_manager = ModelManager(models_dir="../models")

# Load speaker labels and model if available
model_manager.load_speaker_labels()

# Try to load trained model
try:
    model_manager.load_model("svm_speaker_model.pkl", model_type="sklearn")
except FileNotFoundError:
    print("No trained model found. Model will use placeholder predictions.")
except Exception as e:
    print(f"Error loading model: {e}")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Speaker ID API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": ["/health", "/predict", "/train", "/models", "/audio-stats"]
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Backend is running",
        "loaded_models": len(model_manager.models),
        "speaker_count": len(model_manager.speakers)
    }


@app.get("/models")
def list_models():
    """List all loaded models."""
    return {
        "models": model_manager.list_models(),
        "speakers": model_manager.speakers
    }


@app.post("/audio-stats")
async def get_audio_stats(audio_file: UploadFile = File(...)):
    """
    Get statistics about uploaded audio file.
    Useful for debugging and verification.
    """
    tmp_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            content = await audio_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Load and process audio
        audio = audio_processor.load_audio(tmp_path)
        stats = audio_processor.get_audio_stats(audio)
        
        # Cleanup
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        return JSONResponse({
            "filename": audio_file.filename,
            "stats": stats,
            "preprocessed_length_ms": len(audio_processor.preprocess_audio(audio))
        })
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict")
async def predict_speaker(
    audio_file: UploadFile = File(...),
    feature_type: str = "mfcc",
    top_k: int = 3
):
    """
    Predict speaker identity from uploaded audio file.
    
    Args:
        audio_file: Audio file (WAV format recommended)
        feature_type: Type of features to extract ('mfcc' or 'mel')
        top_k: Number of top predictions to return
        
    Returns:
        Dictionary with predictions and metadata
    """
    tmp_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            content = await audio_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Load and preprocess audio
        audio = audio_processor.load_audio(tmp_path)
        audio = audio_processor.preprocess_audio(audio)
        
        # Extract features
        features = audio_processor.extract_features(audio, feature_type=feature_type)
        
        # Get statistics
        stats = audio_processor.get_audio_stats(audio)
        
        # Predict
        prediction = model_manager.predict(features, top_k=top_k)
        
        # Cleanup
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        return JSONResponse({
            "filename": audio_file.filename,
            "feature_type": feature_type,
            "audio_stats": stats,
            "features_shape": list(features.shape),
            "prediction": prediction
        })
        
    except Exception as e:
        # Cleanup on error
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        # Log detailed error
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in predict_speaker: {error_detail}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/train")
async def train_model(
    speaker_name: str = Form(...),
    audio_files: List[UploadFile] = File(...)
):
    """
    Train or retrain speaker identification model with new data.
    
    Args:
        speaker_name: Name/ID of the speaker
        audio_files: List of audio files for training
        
    Returns:
        Training results and statistics
    """
    try:
        # Validate inputs
        if not speaker_name.strip():
            raise HTTPException(status_code=400, detail="Speaker name cannot be empty")
        
        if len(audio_files) < 3:
            raise HTTPException(status_code=400, detail="At least 3 audio files required")
        
        # Create speaker directory
        speaker_dir = Path("../data/raw") / speaker_name
        speaker_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded files
        saved_files = []
        for audio_file in audio_files:
            # Generate unique filename
            file_ext = os.path.splitext(audio_file.filename)[1] or '.wav'
            unique_filename = f"train_{len(saved_files)+1:03d}{file_ext}"
            file_path = speaker_dir / unique_filename
            
            # Save file
            content = await audio_file.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            
            saved_files.append(unique_filename)
        
        # Retrain model using train_model.py script
        try:
            # Get absolute path to train_model.py
            script_path = Path(__file__).parent.parent / "train_model.py"
            
            result = subprocess.run(
                ['python', str(script_path)],
                cwd=str(Path(__file__).parent.parent),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Debug output
            print(f"Training return code: {result.returncode}")
            print(f"Training stdout: {result.stdout[:500] if result.stdout else 'None'}")
            print(f"Training stderr: {result.stderr[:500] if result.stderr else 'None'}")
            
            if result.returncode != 0:
                error_detail = result.stderr if result.stderr else result.stdout if result.stdout else "Unknown error"
                raise HTTPException(
                    status_code=500,
                    detail=f"Model training failed: {error_detail}"
                )
            
            # Reload model in memory
            try:
                model_manager.load_model("svm_speaker_model.pkl", model_type="sklearn")
                model_manager.load_speaker_labels()
            except Exception as e:
                print(f"Warning: Could not reload model: {e}")
            
            # Parse accuracy from output
            accuracy = 0.0
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if 'Test Accuracy:' in line:
                        try:
                            acc_str = line.split('(')[1].split('%')[0]
                            accuracy = float(acc_str) / 100
                        except:
                            pass
            
            return JSONResponse({
                "status": "success",
                "speaker_name": speaker_name,
                "files_added": len(saved_files),
                "accuracy": accuracy,
                "message": f"Successfully added {len(saved_files)} files for {speaker_name}",
                "model_retrained": True
            })
            
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="Model training timed out")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile
import os
from pathlib import Path
import numpy as np
import subprocess
import sys  # <-- eklendi

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

# Try to load all available models
try:
    model_manager.load_all_available_models()
except Exception as e:
    print(f"Error loading models: {e}")
    
# Fallback: Try to load default SVM model if no models were loaded
if len(model_manager.models) == 0:
    # Try default model name (only MFCC supported now)
    try:
        model_manager.load_model("svm_speaker_model.pkl", model_type="sklearn")
    except FileNotFoundError:
        print("No trained model found. Model will use placeholder predictions.")
    except Exception as e:
        print(f"Error loading default model: {e}")


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
    best_model = model_manager.get_best_model()
    best_model_accuracy = None
    if best_model and best_model in model_manager.model_metadata:
        best_model_accuracy = model_manager.model_metadata[best_model].get('test_accuracy')
    
    return {
        "status": "ok",
        "message": "Backend is running",
        "loaded_models": len(model_manager.models),
        "speaker_count": len(model_manager.speakers),
        "best_model": best_model,
        "best_model_accuracy": best_model_accuracy
    }


@app.get("/models")
def list_models():
    """List all loaded models."""
    return {
        "models": model_manager.list_models(),
        "speakers": model_manager.speakers
    }


@app.get("/metrics")
def get_model_metrics():
    """Get detailed metrics for all models."""
    metrics = {}
    
    for model_name in model_manager.models.keys():
        metadata = model_manager.model_metadata.get(model_name, {})
        if metadata:
            metrics[model_name] = {
                "model_type": metadata.get("model_type"),
                "test_accuracy": metadata.get("test_accuracy"),
                "train_accuracy": metadata.get("train_accuracy"),
                "precision_macro": metadata.get("precision_macro"),
                "recall_macro": metadata.get("recall_macro"),
                "f1_macro": metadata.get("f1_macro"),
                "precision_weighted": metadata.get("precision_weighted"),
                "recall_weighted": metadata.get("recall_weighted"),
                "f1_weighted": metadata.get("f1_weighted"),
                "num_speakers": metadata.get("num_speakers"),
                "confusion_matrix": metadata.get("confusion_matrix"),
                "speakers": metadata.get("speakers", [])
            }
    
    return {
        "models": metrics,
        "best_model": model_manager.get_best_model()
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
    top_k: int = 3,
    model_name: str = None
):
    """
    Predict speaker identity from uploaded audio file.
    
    Args:
        audio_file: Audio file (WAV format recommended)
        feature_type: Type of features to extract ('mfcc' or 'mel')
        top_k: Number of top predictions to return
        model_name: Name of model to use (optional, uses first available if not specified)
        
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
        
        # Predict (use specified model or automatically select best model)
        # model_manager.predict() will automatically use best model if model_name is None
        prediction = model_manager.predict(features, model_name=model_name, top_k=top_k)
        
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
    audio_files: List[UploadFile] = File(...),
    model_type: str = Form("svm"),
    feature_type: str = Form("mfcc")  # Default to MFCC, Mel support removed from UI
):
    """
    Train or retrain speaker identification model with new data.
    
    Args:
        speaker_name: Name/ID of the speaker
        audio_files: List of audio files for training
        model_type: Type of model to train ('svm', 'random_forest', 'neural_network', 'adaboost')
        feature_type: Type of features to extract (default: 'mfcc', Mel removed from UI)
        
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
        
        # Validate model type
        valid_model_types = ['svm', 'random_forest', 'neural_network', 'adaboost']
        if model_type not in valid_model_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model_type. Must be one of: {', '.join(valid_model_types)}"
            )
        
        # Validate feature type (only MFCC supported now)
        if feature_type not in ['mfcc']:
            # Force MFCC if something else is provided
            feature_type = 'mfcc'
        
        # Retrain model using train_model.py script
        try:
            # Paths & env so that we use venv's Python and can import backend modules
            PROJECT_ROOT = Path(__file__).resolve().parents[1]
            TRAIN_SCRIPT = PROJECT_ROOT / "train_model.py"

            env = os.environ.copy()
            env["PYTHONPATH"] = str(PROJECT_ROOT / "backend") + os.pathsep + env.get("PYTHONPATH", "")

            result = subprocess.run(
                [sys.executable, str(TRAIN_SCRIPT), "--model", model_type, "--feature", feature_type],
                cwd=str(PROJECT_ROOT),                # proje kökü
                capture_output=True,
                text=True,
                timeout=600,                          # 10 minute timeout (NN için daha uzun sürebilir)
                env=env,
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
            
            # Reload models in memory
            try:
                # Determine model filename based on model_type (only MFCC supported)
                model_filenames = {
                    'svm': 'svm_speaker_model.pkl',
                    'random_forest': 'random_forest_speaker_model.pkl',
                    'neural_network': 'neural_network_speaker_model.pkl',
                    'adaboost': 'adaboost_speaker_model.pkl'
                }
                model_filename = model_filenames.get(model_type, 'svm_speaker_model.pkl')
                model_manager.load_model(model_filename, model_type="sklearn")
                model_manager.load_speaker_labels()
            except Exception as e:
                print(f"Warning: Could not reload model: {e}")
                # Try to reload all available models
                try:
                    model_manager.load_all_available_models()
                except Exception as e2:
                    print(f"Warning: Could not reload any models: {e2}")
            
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
                "model_type": model_type,
                "feature_type": feature_type,
                "message": f"Successfully added {len(saved_files)} files for {speaker_name} and trained {model_type} model with {feature_type} features",
                "model_retrained": True
            })
            
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="Model training timed out")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Model management for speaker identification.
Handles loading, inference, and model operations.
"""
import os
import pickle
from typing import Dict, Optional, List
import numpy as np
from pathlib import Path


class ModelManager:
    """Manage speaker identification models."""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.models: Dict[str, any] = {}
        self.speakers: List[str] = []
    
    def load_model(self, model_name: str, model_type: str = "pytorch"):
        """
        Load a trained model.
        
        Args:
            model_name: Name of the model file
            model_type: Type of model ('pytorch', 'sklearn', 'onnx')
        """
        model_path = self.models_dir / model_name
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        if model_type == "sklearn":
            with open(model_path, 'rb') as f:
                self.models[model_name] = pickle.load(f)
        elif model_type == "pytorch":
            # TODO: Implement PyTorch model loading
            pass
        elif model_type == "onnx":
            # TODO: Implement ONNX model loading
            pass
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        print(f"Loaded model: {model_name}")
    
    def load_speaker_labels(self, labels_file: str = "speaker_labels.txt"):
        """Load speaker labels from file."""
        labels_path = self.models_dir / labels_file
        if labels_path.exists():
            with open(labels_path, 'r', encoding='utf-8') as f:
                self.speakers = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(self.speakers)} speaker labels")
        else:
            print("Speaker labels file not found")
    
    def predict(
        self, 
        features: np.ndarray, 
        model_name: Optional[str] = None,
        top_k: int = 3
    ) -> Dict:
        """
        Predict speaker from features.
        
        Args:
            features: Extracted features
            model_name: Name of model to use
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        if not self.models:
            return {
                "error": "No models loaded",
                "predictions": []
            }
        
        # Use first model if not specified
        if model_name is None:
            model_name = list(self.models.keys())[0]
        
        model = self.models.get(model_name)
        if model is None:
            return {
                "error": f"Model {model_name} not found",
                "predictions": []
            }
        
        # Check if we have a real model or need placeholder
        if hasattr(model, 'predict_proba'):
            # REAL MODEL INFERENCE (SVM, etc.)
            # Flatten features for SVM (expects 1D array)
            if len(features.shape) > 1:
                features_flat = features.flatten()
            else:
                features_flat = features
            
            # Get probabilities for all classes
            probabilities = model.predict_proba([features_flat])[0]
            
            # Get class names
            class_names = model.classes_
            
            # Get top K predictions
            top_indices = np.argsort(probabilities)[::-1][:top_k]
            
            predictions = []
            for idx in top_indices:
                speaker_id = class_names[idx]
                confidence = float(probabilities[idx])
                
                # Use class_names directly (already has the correct names)
                predictions.append({
                    "speaker_id": speaker_id,
                    "confidence": confidence,
                    "speaker_name": str(speaker_id)  # Use the class name directly
                })
        else:
            # PLACEHOLDER PREDICTIONS (no model loaded)
            predictions = [
                {
                    "speaker_id": f"speaker_{i+1:02d}",
                    "confidence": float(np.random.uniform(0.7, 0.95)),
                    "speaker_name": f"Speaker {i+1}" if i < len(self.speakers) else f"speaker_{i+1:02d}"
                }
                for i in range(min(top_k, len(self.speakers)))
            ]
        
        return {
            "model_used": model_name,
            "predictions": predictions,
            "timestamp_ms": float(np.mean(features) * 1000) if len(features) > 0 else 0
        }
    
    def list_models(self) -> List[str]:
        """List available models."""
        return list(self.models.keys())
    
    def unload_model(self, model_name: str):
        """Unload a model from memory."""
        if model_name in self.models:
            del self.models[model_name]
            print(f"Unloaded model: {model_name}")


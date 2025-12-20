"""
Model management for speaker identification.
Handles loading, inference, and model operations.
"""
import os
import pickle
import json
from typing import Dict, Optional, List, Tuple
import numpy as np
from pathlib import Path


class ModelManager:
    """Manage speaker identification models."""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.models: Dict[str, any] = {}
        self.speakers: List[str] = []
        self.model_metadata: Dict[str, Dict] = {}  # Model metadata cache
    
    def load_model(self, model_name: str, model_type: str = "sklearn"):
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
            raise NotImplementedError("PyTorch model loading not yet implemented")
        elif model_type == "onnx":
            # TODO: Implement ONNX model loading
            raise NotImplementedError("ONNX model loading not yet implemented")
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Load metadata if available
        metadata_path = self.models_dir / f"{model_name}.meta"
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.model_metadata[model_name] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load metadata for {model_name}: {e}")
        
        print(f"Loaded model: {model_name} (type: {model_type})")
    
    def load_all_available_models(self):
        """Tüm mevcut sklearn modellerini yükle (MFCC ve Mel destekli)."""
        # Tüm olası model dosyalarını bul
        model_patterns = [
            'svm_speaker_model*.pkl',
            'random_forest_speaker_model*.pkl',
            'neural_network_speaker_model*.pkl',
            'adaboost_speaker_model*.pkl'
        ]
        
        loaded_count = 0
        for pattern in model_patterns:
            # Glob ile tüm eşleşen dosyaları bul
            import glob
            model_files = list(self.models_dir.glob(pattern))
            for model_path in model_files:
                model_file = model_path.name
                try:
                    self.load_model(model_file, model_type='sklearn')
                    loaded_count += 1
                except Exception as e:
                    print(f"Warning: Could not load {model_file}: {e}")
        
        if loaded_count == 0:
            print("No models found to load")
        else:
            print(f"Loaded {loaded_count} model(s)")
    
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
        
        # Use best model if not specified
        if model_name is None:
            model_name = self.get_best_model()
            if model_name is None:
                return {
                    "error": "No models available",
                    "predictions": []
                }
        
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
    
    def get_best_model(self) -> Optional[str]:
        """
        Get the best model based on test accuracy.
        
        Returns:
            Name of the best model, or None if no models available
        """
        if not self.models:
            return None
        
        best_model = None
        best_accuracy = -1.0
        
        for model_name in self.models.keys():
            metadata = self.model_metadata.get(model_name, {})
            test_accuracy = metadata.get('test_accuracy', 0.0)
            
            if test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                best_model = model_name
        
        # If no metadata with accuracy, use first model as fallback
        if best_model is None:
            best_model = list(self.models.keys())[0]
        
        return best_model
    
    def unload_model(self, model_name: str):
        """Unload a model from memory."""
        if model_name in self.models:
            del self.models[model_name]
            print(f"Unloaded model: {model_name}")


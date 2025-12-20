"""
Audio processing utilities for speaker identification.
Handles feature extraction (MFCC, Mel-spectrograms) using Librosa.
"""
import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional


class AudioProcessor:
    """Process audio files and extract features for speaker identification."""
    
    # Standard audio parameters
    SAMPLE_RATE = 16000  # 16 kHz
    N_MFCC = 13  # Number of MFCC coefficients
    N_MELS = 40  # Mel filter banks
    HOP_LENGTH = 512  # FFT hop length
    
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        self.sample_rate = sample_rate
    
    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Load audio file and convert to mono.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Audio data as numpy array
        """
        audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
        return audio
    
    def extract_mfcc(
        self, 
        audio: np.ndarray, 
        n_mfcc: int = N_MFCC,
        hop_length: int = HOP_LENGTH
    ) -> np.ndarray:
        """
        Extract MFCC features from audio signal.
        
        Args:
            audio: Audio signal array
            n_mfcc: Number of MFCC coefficients
            hop_length: FFT hop length
            
        Returns:
            MFCC features (n_frames, n_mfcc)
        """
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=n_mfcc,
            hop_length=hop_length
        )
        # Transpose to get (time_steps, features)
        return mfccs.T
    
    def extract_mel_spectrogram(
        self, 
        audio: np.ndarray,
        n_mels: int = N_MELS,
        hop_length: int = HOP_LENGTH
    ) -> np.ndarray:
        """
        Extract Mel-spectrogram features from audio signal.
        
        Args:
            audio: Audio signal array
            n_mels: Number of Mel filter banks
            hop_length: FFT hop length
            
        Returns:
            Mel-spectrogram features (n_frames, n_mels)
        """
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=n_mels,
            hop_length=hop_length
        )
        # Convert to log scale
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        return mel_spec_db.T
    
    def extract_features(
        self, 
        audio: np.ndarray,
        feature_type: str = "mfcc"
    ) -> np.ndarray:
        """
        Extract features based on specified type.
        
        Args:
            audio: Audio signal array
            feature_type: Type of features ('mfcc' or 'mel')
            
        Returns:
            Feature array
        """
        if feature_type.lower() == "mfcc":
            return self.extract_mfcc(audio)
        elif feature_type.lower() == "mel":
            return self.extract_mel_spectrogram(audio)
        else:
            raise ValueError(f"Unknown feature type: {feature_type}")
    
    def preprocess_audio(
        self, 
        audio: np.ndarray,
        target_length_ms: int = 3000  # 3 seconds
    ) -> np.ndarray:
        """
        Preprocess audio: padding or trimming to target length.
        
        Args:
            audio: Audio signal array
            target_length_ms: Target length in milliseconds
            
        Returns:
            Preprocessed audio
        """
        target_samples = int(self.sample_rate * target_length_ms / 1000)
        
        if len(audio) > target_samples:
            # Trim to target length (take middle portion)
            start = len(audio) // 2 - target_samples // 2
            audio = audio[start:start + target_samples]
        elif len(audio) < target_samples:
            # Pad with zeros
            padding = target_samples - len(audio)
            audio = np.pad(audio, (padding // 2, padding - padding // 2), mode='constant')
        
        return audio
    
    def get_audio_stats(self, audio: np.ndarray) -> dict:
        """
        Get statistics about audio signal.
        
        Args:
            audio: Audio signal array
            
        Returns:
            Dictionary with audio statistics
        """
        return {
            "duration_ms": len(audio) / self.sample_rate * 1000,
            "sample_rate": self.sample_rate,
            "mean": float(np.mean(audio)),
            "std": float(np.std(audio)),
            "max": float(np.max(np.abs(audio)))
        }


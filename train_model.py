"""
Basit konuşmacı tanıma modeli eğitim scripti.
SVM kullanarak MFCC özellikleri üzerinde eğitim yapar.
"""
import sys
import os
sys.path.append('backend')

# Windows encoding fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from audio_processor import AudioProcessor

def train_speaker_model():
    """Ana eğitim fonksiyonu."""
    
    print("🎤 Speaker Identification Model Training")
    print("=" * 50)
    
    # Yollar
    data_dir = Path("data/raw")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Audio processor
    processor = AudioProcessor()
    
    # Veri yükleme
    print("\n📂 Loading audio files...")
    features_list = []
    labels_list = []
    
    if not data_dir.exists():
        print(f"❌ Error: {data_dir} directory not found!")
        print("\nPlease create the following structure:")
        print("data/raw/")
        print("  speaker_01/")
        print("    utt_0001.wav")
        print("    utt_0002.wav")
        print("  speaker_02/")
        print("    utt_0001.wav")
        return
    
    # Find all directories (not just speaker_* prefix)
    speaker_folders = sorted([d for d in data_dir.iterdir() if d.is_dir()])
    
    if len(speaker_folders) == 0:
        print(f"❌ Error: No speaker folders found in {data_dir}")
        print("Expected folders like: speaker_01, speaker_02, etc.")
        return
    
    print(f"Found {len(speaker_folders)} speakers:")
    
    for speaker_folder in speaker_folders:
        speaker_name = speaker_folder.name
        # Support multiple audio formats
        audio_files = (list(speaker_folder.glob('*.wav')) + 
                      list(speaker_folder.glob('*.mp3')) +
                      list(speaker_folder.glob('*.m4a')) +
                      list(speaker_folder.glob('*.webm')) +
                      list(speaker_folder.glob('*.ogg')))
        
        if len(audio_files) == 0:
            print(f"  ⚠️  {speaker_name}: No audio files found")
            continue
        
        print(f"  ✅ {speaker_name}: {len(audio_files)} files")
        
        # Her ses dosyasını işle
        for audio_file in audio_files:
            try:
                # Yükle ve ön işle
                audio = processor.load_audio(str(audio_file))
                audio = processor.preprocess_audio(audio)  # 3 saniyeye normalize et
                
                # MFCC özelliklerini çıkar
                mfcc_features = processor.extract_mfcc(audio)
                
                # Düzleştir (SVM için)
                features_flat = mfcc_features.flatten()
                
                features_list.append(features_flat)
                labels_list.append(speaker_name)
                
            except Exception as e:
                print(f"     ⚠️  Failed to process {audio_file.name}: {e}")
                continue
    
    if len(features_list) == 0:
        print("\n❌ Error: No valid audio files found!")
        return
    
    # NumPy dizilerine çevir
    X = np.array(features_list)
    y = np.array(labels_list)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features per sample: {X.shape[1]}")
    print(f"   Unique speakers: {len(np.unique(y))}")
    
    # Check if we have at least 2 speakers
    if len(np.unique(y)) < 2:
        print("\n❌ Error: Need at least 2 different speakers!")
        print("Please add audio files for another speaker before training.")
        print("Model training requires multiple classes.")
        return
    
    # Veriyi böl
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n🔬 Train/Test Split:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    
    # Model eğitimi
    print(f"\n🤖 Training SVM model...")
    svm_model = SVC(kernel='rbf', probability=True, random_state=42)
    svm_model.fit(X_train, y_train)
    
    # Değerlendirme
    train_score = svm_model.score(X_train, y_train)
    test_score = svm_model.score(X_test, y_test)
    
    print(f"\n📈 Model Performance:")
    print(f"   Train Accuracy: {train_score:.4f} ({train_score*100:.2f}%)")
    print(f"   Test Accuracy: {test_score:.4f} ({test_score*100:.2f}%)")
    
    # Test tahminleri
    y_pred = svm_model.predict(X_test)
    
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print(f"\n🎯 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Modeli kaydet
    model_path = models_dir / 'svm_speaker_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(svm_model, f)
    print(f"\n💾 Model saved to: {model_path}")
    
    # Speaker labels kaydet
    unique_speakers = sorted(np.unique(y))
    labels_path = models_dir / 'speaker_labels.txt'
    with open(labels_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_speakers))
    print(f"📝 Speaker labels saved to: {labels_path}")
    
    print("\n✅ Training complete!")
    print(f"\nNow you can use the model in the backend:")
    print(f"  - Model file: models/svm_speaker_model.pkl")
    print(f"  - Labels: models/speaker_labels.txt")

if __name__ == "__main__":
    train_speaker_model()


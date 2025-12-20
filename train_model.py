"""
Konuşmacı tanıma modeli eğitim scripti.
Farklı ML algoritmaları ile MFCC özellikleri üzerinde eğitim yapar.
Desteklenen modeller: SVM, Random Forest, Neural Network, AdaBoost
"""
import sys
import os
import argparse
from pathlib import Path

# Add backend directory to Python path
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Windows encoding fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
from audio_processor import AudioProcessor  # type: ignore

def create_model(model_type: str, random_state: int = 42):
    """
    Model oluştur.
    
    Args:
        model_type: Model tipi ('svm', 'random_forest', 'neural_network', 'adaboost')
        random_state: Rastgelelik durumu
        
    Returns:
        Eğitilmemiş model
    """
    if model_type == 'svm':
        return SVC(kernel='rbf', probability=True, random_state=random_state)
    elif model_type == 'random_forest':
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=random_state,
            n_jobs=-1
        )
    elif model_type == 'neural_network':
        return MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='constant',
            learning_rate_init=0.001,
            max_iter=500,
            random_state=random_state,
            early_stopping=True,
            validation_fraction=0.1
        )
    elif model_type == 'adaboost':
        return AdaBoostClassifier(
            n_estimators=50,
            learning_rate=1.0,
            random_state=random_state
        )
    else:
        raise ValueError(f"Bilinmeyen model tipi: {model_type}")


def get_model_filename(model_type: str, feature_type: str = 'mfcc') -> str:
    """Model dosya adını döndür (sadece MFCC kullanılıyor)."""
    base_names = {
        'svm': 'svm',
        'random_forest': 'random_forest',
        'neural_network': 'neural_network',
        'adaboost': 'adaboost'
    }
    base_name = base_names.get(model_type, 'model')
    return f'{base_name}_speaker_model.pkl'


def train_speaker_model(model_type: str = 'svm', feature_type: str = 'mfcc'):
    """
    Ana eğitim fonksiyonu.
    
    Args:
        model_type: Model tipi ('svm', 'random_forest', 'neural_network', 'adaboost')
        feature_type: Özellik tipi ('mfcc' - Mel desteği kaldırıldı)
    """
    model_names = {
        'svm': 'SVM (Support Vector Machine)',
        'random_forest': 'Random Forest',
        'neural_network': 'Neural Network (MLP)',
        'adaboost': 'AdaBoost'
    }
    
    feature_names = {
        'mfcc': 'MFCC (Mel-Frequency Cepstral Coefficients)',
        'mel': 'Mel-Spectrogram'
    }
    
    # Validate feature type (only MFCC supported)
    if feature_type not in ['mfcc']:
        print(f"⚠️  Warning: feature_type '{feature_type}' not supported. Using 'mfcc' instead.")
        feature_type = 'mfcc'
    
    print("🎤 Speaker Identification Model Training")
    print("=" * 50)
    print(f"📦 Model Tipi: {model_names.get(model_type, model_type)}")
    print(f"🎵 Özellik Tipi: {feature_names.get(feature_type, feature_type)}")
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
                
                # Özellikleri çıkar (sadece MFCC kullanılıyor)
                features = processor.extract_mfcc(audio)
                
                # Düzleştir (ML modelleri için)
                features_flat = features.flatten()
                
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
    
    # Model oluştur ve eğit
    print(f"\n🤖 Training {model_names.get(model_type, model_type)} model...")
    model = create_model(model_type)
    model.fit(X_train, y_train)
    
    # Değerlendirme
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\n📈 Model Performance:")
    print(f"   Train Accuracy: {train_score:.4f} ({train_score*100:.2f}%)")
    print(f"   Test Accuracy: {test_score:.4f} ({test_score*100:.2f}%)")
    
    # Test tahminleri
    y_pred = model.predict(X_test)
    
    # Detaylı metrikler hesapla
    
    # Macro average (tüm sınıflar için ortalama)
    precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    # Weighted average (sınıf büyüklüğüne göre ağırlıklı)
    precision_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print(f"\n🎯 Confusion Matrix:")
    print(cm)
    
    print(f"\n📊 Detailed Metrics:")
    print(f"   Precision (Macro): {precision_macro:.4f}")
    print(f"   Recall (Macro): {recall_macro:.4f}")
    print(f"   F1-Score (Macro): {f1_macro:.4f}")
    
    # Modeli kaydet
    model_filename = get_model_filename(model_type, feature_type)
    model_path = models_dir / model_filename
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n💾 Model saved to: {model_path}")
    
    # Model metadata kaydet (detaylı metrikler ile)
    metadata = {
        'model_type': model_type,
        'feature_type': feature_type,
        'feature_shape': X.shape[1],
        'num_speakers': len(np.unique(y)),
        'test_accuracy': float(test_score),
        'train_accuracy': float(train_score),
        'precision_macro': float(precision_macro),
        'recall_macro': float(recall_macro),
        'f1_macro': float(f1_macro),
        'precision_weighted': float(precision_weighted),
        'recall_weighted': float(recall_weighted),
        'f1_weighted': float(f1_weighted),
        'confusion_matrix': cm.tolist(),  # JSON serializable yapmak için
        'speakers': sorted(np.unique(y).tolist())  # Konuşmacı listesi
    }
    metadata_path = models_dir / f'{model_filename}.meta'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(metadata, f, indent=2)
    print(f"📋 Model metadata saved to: {metadata_path}")
    
    # Speaker labels kaydet
    unique_speakers = sorted(np.unique(y))
    labels_path = models_dir / 'speaker_labels.txt'
    with open(labels_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_speakers))
    print(f"📝 Speaker labels saved to: {labels_path}")
    
    print("\n✅ Training complete!")
    print(f"\nNow you can use the model in the backend:")
    print(f"  - Model file: models/{model_filename}")
    print(f"  - Feature type: {feature_type}")
    print(f"  - Labels: models/speaker_labels.txt")
    print(f"\n💡 Backend'de modeli yüklemek için:")
    print(f"   model_manager.load_model('{model_filename}', model_type='sklearn')")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Konuşmacı tanıma modeli eğitimi')
    parser.add_argument(
        '--model',
        type=str,
        default='svm',
        choices=['svm', 'random_forest', 'neural_network', 'adaboost'],
        help='Eğitilecek model tipi (default: svm)'
    )
    parser.add_argument(
        '--feature',
        type=str,
        default='mfcc',
        choices=['mfcc'],  # Mel desteği kaldırıldı
        help='Kullanılacak özellik tipi: mfcc (default: mfcc, Mel desteği kaldırıldı)'
    )
    
    args = parser.parse_args()
    train_speaker_model(model_type=args.model, feature_type=args.feature)


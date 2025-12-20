# 🎤 Model Eğitim Kılavuzu

Bu kılavuz, konuşmacı tanıma modelini nasıl eğiteceğinizi adım adım açıklar.

## 📋 Gereksinimler

1. Python 3.9+ yüklü olmalı
2. Backend bağımlılıkları yüklü olmalı
3. Ses dosyalarınız hazır olmalı

## 🗂️ Ses Dosyaları Hazırlama

### Klasör Yapısı

Ses dosyalarınızı şu yapıda organize edin:

```
data/
└── raw/
    ├── speaker_01/
    │   ├── utt_0001.wav
    │   ├── utt_0002.wav
    │   ├── utt_0003.wav
    │   └── ...
    ├── speaker_02/
    │   ├── utt_0001.wav
    │   ├── utt_0002.wav
    │   └── ...
    └── speaker_03/
        ├── utt_0001.wav
        └── ...
```

### Ses Dosyası Formatı

- **Format**: WAV (önerilen)
- **Sample Rate**: 16 kHz (otomatik dönüştürülür)
- **Kanal**: Mono (otomatik dönüştürülür)
- **Süre**: En az 1 saniye, ideal 3 saniye

## 🚀 Model Eğitimi

### 1. Backend Bağımlılıklarını Yükleyin

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate    # Windows
# veya
source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

### 2. Eğitim Scriptini Çalıştırın

```bash
# Projenin ana dizininde (backend/ üstünde)
python train_model.py
```

### 3. Çıktıları İnceleyin

Script şu bilgileri gösterecek:

```
🎤 Speaker Identification Model Training
==================================================

📂 Loading audio files...
Found 3 speakers:
  ✅ speaker_01: 15 files
  ✅ speaker_02: 12 files
  ✅ speaker_03: 18 files

📊 Dataset Statistics:
   Total samples: 45
   Features per sample: 1222
   Unique speakers: 3

🔬 Train/Test Split:
   Training samples: 36
   Test samples: 9

🤖 Training SVM model...

📈 Model Performance:
   Train Accuracy: 0.9722 (97.22%)
   Test Accuracy: 0.8889 (88.89%)

💾 Model saved to: models/svm_speaker_model.pkl
📝 Speaker labels saved to: models/speaker_labels.txt

✅ Training complete!
```

### 4. Model Dosyalarını Kontrol Edin

Eğitim tamamlandıktan sonra:

```
models/
├── svm_speaker_model.pkl    # Eğitilmiş model
└── speaker_labels.txt        # Konuşmacı etiketleri
```

`speaker_labels.txt` dosyası şöyle görünür:

```
speaker_01
speaker_02
speaker_03
```

## 🎯 Backend'i Yeniden Başlatın

Model eğitildikten sonra backend'i yeniden başlatın:

```bash
cd backend
.\venv\Scripts\activate
uvicorn app:app --reload
```

Backend başlatılırken şu mesajı göreceksiniz:

```
Loaded model: svm_speaker_model.pkl
Loaded 3 speaker labels
```

## 🧪 Test Edin

### 1. Frontend'i Başlatın

```bash
cd frontend
npm run dev
```

### 2. Tarayıcıda Açın

`http://localhost:3000`

### 3. Ses Kaydedin

1. Mikrofon butonuna tıklayın
2. 3-5 saniye konuşun
3. Durdurun

### 4. Sonuçları Görün

Model artık gerçek tahmin yapacak:

```json
{
  "predictions": [
    {
      "speaker_id": "speaker_01",
      "confidence": 0.87,
      "speaker_name": "speaker_01"
    },
    {
      "speaker_id": "speaker_02",
      "confidence": 0.12,
      "speaker_name": "speaker_02"
    }
  ]
}
```

## 📊 Model Performansı

### İyi Performans İçin

- **Her konuşmacı için minimum 10-15 örnek**
- **Örnekler arasında varyasyon** (farklı ifadeler, tonlar)
- **Kaliteli ses kayıtları** (az gürültü)
- **Tekdüze ortam** (aynı mikrofon, odada konuşma)

### Beklenen Doğruluk

- **3-5 konuşmacı**: %85-95 doğruluk
- **10+ konuşmacı**: %75-85 doğruluk
- **Daha fazla örnek = Daha iyi performans**

## 🐛 Sorun Giderme

### "No speaker folders found"

```
❌ Error: No speaker folders found in data/raw
Expected folders like: speaker_01, speaker_02, etc.
```

**Çözüm**: `data/raw/` içinde `speaker_XX/` klasörleri oluşturun.

### "No WAV files found"

```
⚠️  speaker_01: No WAV files found
```

**Çözüm**: Her konuşmacı klasörüne WAV dosyaları ekleyin.

### "Failed to process audio"

```
⚠️  Failed to process utt_0001.wav: ...
```

**Çözüm**: Dosya bozuk olabilir. Başka bir format deneyin.

### Model düşük doğrulukta

**Çözüm**:
- Daha fazla örnek ekleyin
- Ses kalitesini iyileştirin
- Her konuşmacı için farklı ifadeler kaydedin

## 🔄 Modeli Güncelleme

Yeni konuşmacı eklemek veya mevcut veri setini genişletmek için:

1. `data/raw/` içindeki klasörleri güncelleyin
2. `python train_model.py` çalıştırın
3. Backend'i yeniden başlatın

## 📝 Notlar

- **SVM Model**: RBF kernel kullanıyor (radial basis function)
- **Feature Type**: MFCC (13 katsayı × ~94 frame = 1,222 özellik)
- **Train/Test Split**: %80 eğitim, %20 test (rastgele)
- **Cross-validation**: Şu an yok (eklenebilir)

## 🚀 İleri Seviye

### CNN Modeli Eğitimi

SVM yerine CNN kullanmak için:

1. `notebooks/` klasöründe Jupyter Notebook açın
2. `02_model_training.ipynb` dosyasını kullanın
3. CNN modeli daha hassas ama daha yavaş

### Model Optimizasyonu

- **Grid Search**: En iyi hyperparameter'ları bul
- **Cross-validation**: Daha güvenilir performans metrikleri
- **Feature Engineering**: MFCC yerine Mel-spectrogram veya her ikisi

## 📚 Kaynaklar

- [Librosa MFCC Dokümantasyonu](https://librosa.org/doc/latest/feature.html#mfcc)
- [scikit-learn SVM](https://scikit-learn.org/stable/modules/svm.html)
- [Speaker Recognition Tutorial](https://towardsdatascience.com/speaker-recognition-using-mfcc-8f8e1b3f6e5)


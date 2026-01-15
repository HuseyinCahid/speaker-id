# 🎤 Konuşmacı Tanıma Sistemi - Hızlı Başlangıç

## ✅ Sistem Hazır - Nasıl Kullanılır?

## 🌐 Web Üzerinden Model Eğitimi (Önerilen)

En kolay yol: **Web arayüzünden model eğitin!**

### 📝 Adım 1: Sistemleri Başlatın

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 🎓 Adım 2: Web Arayüzünden Eğitin

1. Tarayıcıda `http://localhost:3000` açın
2. **"🎓 Model Eğit"** butonuna tıklayın
3. Konuşmacı adını girin (örn: speaker_01)
4. Ses dosyalarını seçin (en az 3 tane)
5. **"🎓 Modeli Eğit"** butonuna tıklayın
6. Model otomatik olarak eğitilir!

**Detaylı kılavuz:** `WEB_TRAINING_GUIDE.md`

---

## 💻 Komut Satırından Eğitim (Alternatif)

### 📝 Adım 1: Ses Dosyalarınızı Hazırlayın

Ses dosyalarınızı şu şekilde organize edin:

```
speaker-id/
└── data/
    └── raw/
        ├── speaker_01/
        │   ├── kayit_001.wav
        │   ├── kayit_002.wav
        │   └── kayit_003.wav
        ├── speaker_02/
        │   └── kayit_001.wav
        └── speaker_03/
            └── kayit_001.wav
```

### 🎯 Adım 2: Model Eğitin

**Temel Eğitim:**
```bash
python train_model.py
```

**Cross-Validation ile:**
```bash
python train_model.py --cv --cv-folds 5
```

**Hyperparameter Tuning ile:**
```bash
python train_model.py --tune --tuning-method grid
```

**Her İkisi ile (Önerilen):**
```bash
python train_model.py --cv --cv-folds 5 --tune --tuning-method random --n-iter 20
```

**Detaylı kılavuz:** `CROSS_VALIDATION_GUIDE.md` 🆕

Çıktı:
```
🎤 Speaker Identification Model Training
==================================================

📂 Loading audio files...
Found 3 speakers:
  ✅ speaker_01: 10 files
  ✅ speaker_02: 8 files  
  ✅ speaker_03: 12 files

📊 Dataset Statistics:
   Total samples: 30
   Features per sample: 1222
   Unique speakers: 3

🤖 Training SVM model...

📈 Model Performance:
   Train Accuracy: 0.9500 (95.00%)
   Test Accuracy: 0.8333 (83.33%)

💾 Model saved to: models/svm_speaker_model.pkl
📝 Speaker labels saved to: models/speaker_labels.txt

✅ Training complete!
```

### 🚀 Adım 3: Backend'i Başlatın

```bash
cd backend
.\venv\Scripts\activate    # Windows
# veya
source venv/bin/activate   # Linux/Mac

uvicorn app:app --reload
```

**Backend başlatınca şunu göreceksiniz:**
```
Loaded model: svm_speaker_model.pkl
Loaded 3 speaker labels
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 🎨 Adım 4: Frontend'i Başlatın

**Yeni terminal penceresinde:**

```bash
cd frontend
npm run dev
```

### 🌐 Adım 5: Test Edin

1. Tarayıcıda açın: `http://localhost:3000`
2. Mikrofon butonuna basın 🎤
3. 3-5 saniye konuşun
4. Durdur butonuna basın ⏹

**Sonuç:**
```
🏆 Konuşmacı: speaker_01
   Güven: 87%
```

## ❓ Karşılaştırma Nasıl Çalışıyor?

### 1️⃣ **EĞİTİM AŞAMASI** (bir kere yapılır)

```
Eğitim Verileri:
├── Kişi A sesi → MFCC özellikleri → Model'e öğretildi
├── Kişi B sesi → MFCC özellikleri → Model'e öğretildi
└── Kişi C sesi → MFCC özellikleri → Model'e öğretildi

Model: "Şimdi bu 3 kişinin ses özelliklerini biliyorum"
```

### 2️⃣ **TAHMIN AŞAMASI** (her testte)

```
Yeni Ses Kaydı:
├── Kaydedilen ses → MFCC özellikleri → Model
├── Model: Bu özelliklere bakayım...
├── Model: "Kişi A: %87, Kişi B: %8, Kişi C: %5"
└── Sonuç: "Muhtemelen Kişi A!"
```

### 3️⃣ **ALGORITMA**

**SVM (Support Vector Machine)** kullanılıyor:

- **Öğrenme**: Her kişinin MFCC özellikleri "ayrık bölgeler" olarak öğrenilir
- **Karşılaştırma**: Yeni sesin MFCC özellikleri bu bölgelerle karşılaştırılır
- **Mesafe**: Hangi bölgeye daha yakınsa o kişi tahmin edilir

## 📊 Örnek Karşılaştırma

```
Kişi A'nın MFCC Profili (Eğitimden):
[2.3, -1.5, 0.8, 4.2, -2.1, ...]  ← 1222 özellik

Kişi B'nin MFCC Profili (Eğitimden):
[-0.5, 3.2, -2.8, 1.1, 4.5, ...]  ← 1222 özellik

Yeni Ses Kaydı (Test):
[2.1, -1.3, 0.9, 4.0, -2.3, ...]  ← 1222 özellik

SVM Karşılaştırması:
- Kişi A'ya uzaklık: 0.15  (YAKIN!)
- Kişi B'ye uzaklık: 2.87  (UZAK!)

Sonuç: %87 güvenle Kişi A!
```

## 🎯 Başarı İçin İpuçları

### ✅ İYİ YAPILACAKLAR

1. **Her kişi için yeterli veri**
   - Minimum: 5-10 kayıt
   - İdeal: 15-20 kayıt

2. **Farklı ifadeler kaydedin**
   - Normal konuşma
   - Hızlı konuşma
   - Yavaş konuşma

3. **Kaliteli ses**
   - Sessiz ortam
   - Mikrofonu yakın tutun
   - Yüksek sesle konuşun

### ❌ YAPMAYIN

1. **Sadece 1-2 kayıt** - Yeterli değil
2. **Gürültülü ortam** - Kaliteyi düşürür
3. **Çok farklı mikrofonlar** - Tutarlılık bozar
4. **Çok kısa ses** - Özellik çıkarmak zor

## 🔧 Sorun Çözme

### Model bulunamadı

**Hata:**
```
No trained model found. Model will use placeholder predictions.
```

**Çözüm:** `python train_model.py` çalıştırın

### Ses yüklenmiyor

**Hata:**
```
Failed to access microphone
```

**Çözüm:** Tarayıcıda mikrofon izni verin

### Düşük doğruluk

**Çözüm:**
- Daha fazla örnek ekleyin
- Ses kalitesini iyileştirin
- Her kişi için çeşitli örnekler kaydedin

## 📚 Daha Fazla Bilgi

- Web eğitim kılavuzu: `WEB_TRAINING_GUIDE.md` ⭐
- Komut satırı eğitim: `TRAINING_GUIDE.md`
- **Cross-Validation & Tuning: `CROSS_VALIDATION_GUIDE.md`** 🆕
- API dokümantasyonu: `http://localhost:8000/docs`
- Proje durumu: `PROJECT_STATUS.md`

## 🎉 Hazırsınız!

Artık sisteminiz çalışır durumda. **Web arayüzünden** ses dosyalarınızı yükleyin, modeli eğitin ve test edin!


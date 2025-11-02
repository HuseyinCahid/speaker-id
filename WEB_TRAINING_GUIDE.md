# 🌐 Web Üzerinden Model Eğitimi Kılavuzu

## ✅ Sistem Özellikleri

Artık sisteminiz tamamen web tabanlı! Ses dosyalarınızı tarayıcıdan yükleyebilir ve modeli doğrudan eğitebilirsiniz.

## 🚀 Nasıl Kullanılır?

### 1️⃣ Sistemleri Başlatın

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate    # Windows
uvicorn app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Tarayıcıda:** `http://localhost:3000`

### 2️⃣ Model Eğitme Sayfasına Gidin

Ana sayfada **"🎓 Model Eğit"** butonuna tıklayın, veya:
- `http://localhost:3000/train` adresine gidin

### 3️⃣ Konuşmacı Adı Girin

```
Konuşmacı Adı: speaker_01
```

**Önemli:** Benzersiz bir isim kullanın (örn: speaker_01, Ahmet, Maria)

### 4️⃣ Ses Dosyaları Ekleyin

**Seçenek 1: Tek seferde çoklu dosya**
- Dosyaları seçmek için tıklayın
- Ctrl tuşuna basılı tutarak birden fazla dosya seçin

**Seçenek 2: Birden fazla seferde**
- İlk dosyayı seçin
- Yeni dosyalar için tekrar tıklayın
- Sistem otomatik olarak listeye ekler

**Minimum:** En az 3 dosya gerekli (önerilen: 5-10 dosya)

### 5️⃣ Eğitim Başlatın

**"🎓 Modeli Eğit"** butonuna tıklayın

Sistem şunları yapar:
1. ✅ Dosyaları kaydeder (`data/raw/speaker_XX/`)
2. ✅ Modeli eğitir (1-2 dakika)
3. ✅ Sonuçları gösterir

### 6️⃣ Sonuçları Görün

```
✅ Eğitim Tamamlandı!

Konuşmacı: speaker_01
Eklenen Dosya: 8
Model Doğruluğu: 87.5%
```

### 7️⃣ Test Edin!

Ana sayfaya (`/`) geri dönün:
1. Mikrofon butonuna basın 🎤
2. 3-5 saniye konuşun
3. Durdurun
4. Model tahmin yapacak!

## 📊 İş Akışı

```
KULLANICI ARAYÜZÜ (/train)
    ↓
[Ses dosyaları yükle]
    ↓
BACKEND API (/train endpoint)
    ↓
[data/raw/speaker_01/ klasörüne kaydet]
    ↓
[train_model.py scriptini çalıştır]
    ↓
[MODEL EĞİTİMİ]
    ├── MFCC özelliklerini çıkar
    ├── SVM modelini eğit
    ├── Test doğruluğunu hesapla
    └── Modeli kaydet (models/svm_speaker_model.pkl)
    ↓
[Yeni modeli belleğe yükle]
    ↓
SONUÇ GÖSTER
```

## 🎯 Çoklu Konuşmacı Eğitimi

### İlk Konuşmacı

1. Konuşmacı adı: `speaker_01`
2. 5-10 ses dosyası yükleyin
3. Eğit'i tıklayın
4. Sistem model oluşturur

### İkinci Konuşmacı

1. Konuşmacı adı: `speaker_02`
2. 5-10 ses dosyası yükleyin
3. Eğit'i tıklayın
4. Sistem modeli günceller (tüm konuşmacıları öğrenir)

### Üçüncü Konuşmacı

1. Konuşmacı adı: `speaker_03`
2. 5-10 ses dosyası yükleyin
3. Eğit'i tıklayın
4. Sistem 3 konuşmacıyı da tanır!

**Her yeni konuşmacı eklendiğinde model yeniden eğitilir.**

## 📁 Otomatik Klasör Yapısı

Ses dosyaları otomatik olarak şu yapıya kaydedilir:

```
data/raw/
├── speaker_01/
│   ├── train_001.wav    ← Web'den yüklenenler
│   ├── train_002.wav
│   └── train_003.wav
├── speaker_02/
│   ├── train_001.wav
│   └── train_002.wav
└── speaker_03/
    └── train_001.wav
```

## ✅ Kalite Kontrol

### Dosya Formatı
- ✅ WAV (önerilen)
- ✅ MP3
- ✅ M4A
- ✅ WebM

Sistem otomatik olarak dönüştürür.

### Dosya Boyutu
- Minimum: Her dosya için ~100 KB
- İdeal: 200-500 KB (3-5 saniye)

### Ses Kalitesi
- ✅ Sessiz ortam
- ✅ Yakın mikrofon
- ✅ Net konuşma
- ✅ 3-5 saniye uzunluk

## ⚠️ Sorun Giderme

### "At least 3 audio files required"

**Problem:** Yeterli dosya yok  
**Çözüm:** En az 3 ses dosyası seçin

### "Model training failed"

**Problem:** Ses dosyaları bozuk olabilir  
**Çözüm:** 
- Farklı formatlar deneyin
- Dosyaları kontrol edin
- Backend loglarına bakın

### "Model training timed out"

**Problem:** Çok fazla veri, 5 dakikadan uzun sürdü  
**Çözüm:** 
- Daha az dosya ile deneyin
- Timeout süresini artırın (backend/app.py)

### Düşük doğruluk (%50 altı)

**Problem:** Yeterli veri veya kalite eksik  
**Çözüm:**
- Her konuşmacı için 10+ dosya ekleyin
- Ses kalitesini iyileştirin
- Farklı ortamlarda kayıt yapın

## 💡 İpuçları

### Başarılı Eğitim İçin

1. **Her konuşmacı için 10-15 kayıt**
   - Daha fazla veri = Daha iyi performans

2. **Çeşitlilik**
   - Farklı ifadeler
   - Farklı hızlar
   - Farklı tonlar

3. **Tutarlılık**
   - Aynı mikrofon
   - Benzer ortam
   - Benzer mesafe

### İdeal Senaryo

```
Konuşmacı 1: 15 kayıt → Doğruluk: %92
Konuşmacı 2: 12 kayıt → Doğruluk: %88
Konuşmacı 3: 18 kayıt → Doğruluk: %90
========================================
TOPLAM: %90 ortalama doğruluk
```

## 🔄 Model Güncelleme

Model her eğitimde **tamamen yeniden eğitilir**.

**Mevcut veriler:**
- `data/raw/` içindeki TÜM dosyalar
- Otomatik olarak tekrar kullanılır

**Yeni veri ekleme:**
- Aynı konuşmacı için yeni dosyalar ekleyebilirsiniz
- Sistem otomatik olarak modeli günceller

**Veri silme:**
- Manuel olarak `data/raw/` içinden silin
- Sonra eğitim sayfasından tekrar eğitin

## 📊 Performans Metrikleri

Eğitim sonrası gösterilen bilgiler:

```
Test Accuracy: XX.XX%

Bu, modelin test seti üzerindeki doğruluğudur.
- %80+ iyi
- %70-80 kabul edilebilir  
- %50-70 daha fazla veri gerekli
- %50- kötü, yeniden başlayın
```

## 🎉 Artık Hazırsınız!

Web tabanlı eğitim sistemi aktif:
- ✅ Dosya yükleme
- ✅ Otomatik model eğitimi
- ✅ Canlı test
- ✅ Çoklu konuşmacı desteği

**Adımları tekrarlayın:**
1. `/train` sayfasına gidin
2. Konuşmacıları ekleyin
3. Modeli test edin
4. Başarılı olun! 🚀


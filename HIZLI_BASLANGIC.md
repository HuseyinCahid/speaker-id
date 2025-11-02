# ⚡ Hızlı Başlangıç - 5 Dakikada Çalıştırın!

## 🚀 Hemen Başlayın

### 1️⃣ Sistemleri Başlatın

**İki terminal penceresi açın:**

**Terminal 1:**
```bash
cd speaker-id/backend
.\venv\Scripts\activate
uvicorn app:app --reload
```

**Terminal 2:**
```bash
cd speaker-id/frontend
npm run dev
```

### 2️⃣ Tarayıcıda Açın

`http://localhost:3000` → Ana sayfa

### 3️⃣ Model Eğitin

1. "🎓 Model Eğit" butonuna tıklayın
2. Konuşmacı adı: `speaker_01`
3. 3-5 ses dosyası seçin (WAV/MP3/M4A)
4. "🎓 Modeli Eğit" butonuna tıklayın
5. 1-2 dakika bekleyin
6. ✅ Başarılı!

### 4️⃣ Test Edin

1. Ana sayfaya dönün (`/`)
2. 🎤 Mikrofon butonuna basın
3. 3-5 saniye konuşun
4. Durdurun
5. Model tahmin yapacak!

## 🎉 Tamam!

Artık konuşmacı tanıma sisteminiz çalışıyor!

## 📚 Daha Fazla Bilgi

- Detaylı web eğitim: `WEB_TRAINING_GUIDE.md`
- API dokümantasyon: `http://localhost:8000/docs`
- Türkçe kılavuz: `README_TURKCE.md`

## 💡 İpuçları

- Her konuşmacı için 5-10 ses dosyası ideal
- Sessiz ortamda kayıt yapın
- 3-5 saniye uzunluk önerilir
- Daha fazla veri = Daha iyi performans


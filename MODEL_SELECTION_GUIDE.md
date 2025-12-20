# 🔍 Model Seçimi Rehberi

## Tahmin Yaparken Hangi Model Kullanılıyor?

### Mevcut Durum

**Tahmin sırasında model seçimi:**

1. **Backend başlatıldığında:**
   - `load_all_available_models()` çağrılır
   - Tüm mevcut modeller yüklenir (SVM, Random Forest, Neural Network, AdaBoost)

2. **Tahmin yaparken:**
   - Frontend'den `model_name` parametresi gönderilmez
   - Backend'de **ilk yüklenen model** otomatik kullanılır
   - Hangi modelin ilk yükleneceği **belirsizdir** (dosya sistemi sırasına bağlı)

### Sorun

❌ **Belirsizlik:** Hangi modelin kullanıldığı belli değil
❌ **Kontrol yok:** Kullanıcı model seçemiyor
❌ **Tutarsızlık:** Her backend başlatışında farklı model kullanılabilir

---

## 📊 Mevcut Modellerinizi Kontrol Etme

### Backend Loglarına Bakın

Backend başlatıldığında şu çıktıları görürsünüz:

```
Loaded model: svm_speaker_model.pkl (type: sklearn)
Loaded model: random_forest_speaker_model.pkl (type: sklearn)
Loaded 2 model(s)
Loaded 3 speaker labels
```

**İlk yüklenen model** tahminlerde kullanılır.

### API Endpoint ile Kontrol

```bash
# Yüklenen modelleri listele
curl http://localhost:8000/models
```

Çıktı:
```json
{
  "models": [
    "svm_speaker_model.pkl",
    "random_forest_speaker_model.pkl"
  ],
  "speakers": ["Emin Çapa", "Haluk Gürgen", "Çağla Karaali"]
}
```

**İlk model** tahminlerde kullanılır.

---

## ✅ Çözüm Önerileri

### Seçenek 1: Varsayılan Model Belirleme (Önerilen)

Backend'de her zaman belirli bir modeli varsayılan yap:

```python
# backend/app.py'de
DEFAULT_MODEL = "svm_speaker_model.pkl"  # Her zaman SVM kullan

# Tahmin sırasında
prediction = model_manager.predict(
    features, 
    model_name=DEFAULT_MODEL,  # Her zaman SVM
    top_k=top_k
)
```

### Seçenek 2: Frontend'den Model Seçimi

Frontend'e model seçimi dropdown'ı ekle:

```tsx
// Frontend'de
const [selectedModel, setSelectedModel] = useState('svm_speaker_model.pkl');

// API çağrısında
formData.append('model_name', selectedModel);
```

### Seçenek 3: En İyi Modeli Otomatik Seçme

En yüksek doğruluğa sahip modeli otomatik seç (metadata dosyalarından).

---

## 🎯 Hızlı Çözüm

**Şu an için en basit çözüm:** Her zaman SVM modelini kullan.

### Backend'de Değişiklik:

```python
# backend/app.py - predict_speaker() fonksiyonunda
prediction = model_manager.predict(
    features, 
    model_name="svm_speaker_model.pkl",  # Her zaman SVM
    top_k=top_k
)
```

Bu sayede:
- ✅ Her zaman aynı model kullanılır
- ✅ Tutarlı sonuçlar
- ✅ Basit ve anlaşılır

---

## 📝 Notlar

- Birden fazla model eğitilmişse, hangisinin kullanıldığını bilmek önemli
- Farklı modeller farklı doğruluk değerlerine sahip olabilir
- Model seçimi performansı etkileyebilir


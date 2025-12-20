# 🤖 Model Rehberi

Bu dokümanda projede kullanılabilecek farklı makine öğrenmesi modelleri hakkında bilgi bulabilirsiniz.

## 📋 Desteklenen Modeller

### 1. SVM (Support Vector Machine) ⚡
- **Dosya Adı**: `svm_speaker_model.pkl`
- **Hız**: ⭐⭐⭐⭐⭐ Çok Hızlı
- **Doğruluk**: ⭐⭐⭐⭐ İyi
- **Bellek Kullanımı**: ⭐⭐⭐⭐ Düşük
- **Önerilen Kullanım**: Küçük-orta veri setleri, hızlı tahmin gerektiğinde
- **Hyperparameter'lar**: RBF kernel, probability=True

**Avantajlar:**
- Hızlı eğitim süresi
- Küçük model boyutu
- İyi genelleme performansı

**Dezavantajlar:**
- Çok büyük veri setlerinde yavaşlayabilir
- Karmaşık non-linear desenlerde sınırlı

---

### 2. Random Forest 🌲
- **Dosya Adı**: `random_forest_speaker_model.pkl`
- **Hız**: ⭐⭐⭐ Orta
- **Doğruluk**: ⭐⭐⭐⭐ İyi-Çok İyi
- **Bellek Kullanımı**: ⭐⭐⭐ Orta
- **Önerilen Kullanım**: Orta-büyük veri setleri, özellik önemini görmek istediğinizde
- **Hyperparameter'lar**: n_estimators=100, max_depth=20

**Avantajlar:**
- Overfitting'e karşı dirençli
- Feature importance bilgisi
- Paralel işleme desteği (n_jobs=-1)

**Dezavantajlar:**
- Daha büyük model boyutu
- Daha uzun eğitim süresi

---

### 3. Neural Network (MLP) 🧠
- **Dosya Adı**: `neural_network_speaker_model.pkl`
- **Hız**: ⭐⭐ Yavaş (eğitim), ⭐⭐⭐⭐ Hızlı (tahmin)
- **Doğruluk**: ⭐⭐⭐⭐⭐ En İyi
- **Bellek Kullanımı**: ⭐⭐⭐ Orta
- **Önerilen Kullanım**: Büyük veri setleri, maksimum doğruluk istediğinizde
- **Hyperparameter'lar**: 
  - Hidden layers: (128, 64)
  - Activation: ReLU
  - Solver: Adam
  - Max iterations: 500

**Avantajlar:**
- En yüksek doğruluk potansiyeli
- Karmaşık desenleri öğrenebilir
- Early stopping ile overfitting kontrolü

**Dezavantajlar:**
- En uzun eğitim süresi
- Hyperparameter tuning gerektirebilir
- Daha fazla bellek kullanımı

---

### 4. AdaBoost 🚀
- **Dosya Adı**: `adaboost_speaker_model.pkl`
- **Hız**: ⭐⭐⭐⭐ Hızlı
- **Doğruluk**: ⭐⭐⭐⭐ İyi
- **Bellek Kullanımı**: ⭐⭐⭐⭐ Düşük
- **Önerilen Kullanım**: Zayıf öğrenicilerle güçlü modeller oluşturmak
- **Hyperparameter'lar**: n_estimators=50, learning_rate=1.0

**Avantajlar:**
- Hızlı eğitim
- İyi genelleme
- Zayıf sınıflandırıcılarla güçlü modeller

**Dezavantajlar:**
- Aykırı değerlere duyarlı
- Gürültülü verilerde performans düşebilir

---

## 🚀 Kullanım

### Komut Satırından Eğitim

```bash
# SVM modeli (varsayılan)
python train_model.py

# Random Forest
python train_model.py --model random_forest

# Neural Network
python train_model.py --model neural_network

# AdaBoost
python train_model.py --model adaboost
```

### Web Arayüzünden Eğitim

1. `http://localhost:3000/train` sayfasına gidin
2. "Model Tipi" dropdown'ından istediğiniz modeli seçin
3. Konuşmacı adı ve dosyaları girin
4. "Modeli Eğit" butonuna tıklayın

### API Üzerinden Eğitim

```bash
curl -X POST "http://localhost:8000/train" \
  -F "speaker_name=test_speaker" \
  -F "model_type=random_forest" \
  -F "audio_files=@file1.wav" \
  -F "audio_files=@file2.wav"
```

### Tahmin Yaparken Model Seçimi

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "audio_file=@test.wav" \
  -F "model_name=random_forest_speaker_model.pkl"
```

---

## 📊 Model Karşılaştırması

| Model | Eğitim Süresi | Tahmin Süresi | Doğruluk | Model Boyutu |
|-------|--------------|---------------|----------|--------------|
| SVM | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Küçük |
| Random Forest | ⚡⚡⚡ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Orta |
| Neural Network | ⚡⚡ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Orta |
| AdaBoost | ⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Küçük |

---

## 💡 Öneriler

### Hangi Modeli Seçmeliyim?

1. **Küçük Veri Seti (< 100 örnek)**
   - ✅ SVM veya AdaBoost
   - ❌ Neural Network (overfitting riski)

2. **Orta Veri Seti (100-500 örnek)**
   - ✅ Random Forest veya SVM
   - ⚠️ Neural Network (dikkatli kullanın)

3. **Büyük Veri Seti (> 500 örnek)**
   - ✅ Neural Network (en iyi doğruluk)
   - ✅ Random Forest (güvenilir seçenek)

4. **Hız Önemliyse**
   - ✅ SVM veya AdaBoost

5. **Doğruluk Önemliyse**
   - ✅ Neural Network
   - ✅ Random Forest

---

## 🔧 Model Yönetimi

### Backend'de Tüm Modelleri Yükleme

```python
from model_manager import ModelManager

model_manager = ModelManager()
model_manager.load_all_available_models()
```

### Belirli Bir Modeli Yükleme

```python
model_manager.load_model("random_forest_speaker_model.pkl", model_type="sklearn")
```

### Tahmin Yaparken Model Seçimi

```python
# Varsayılan model (ilk yüklenen)
prediction = model_manager.predict(features)

# Belirli bir model
prediction = model_manager.predict(features, model_name="neural_network_speaker_model.pkl")
```

---

## 🎯 Performans İpuçları

1. **Her model için aynı veri setini kullanın** - Adil karşılaştırma için
2. **Cross-validation yapın** - Daha güvenilir metrikler için
3. **Hyperparameter tuning** - Her model için optimal ayarları bulun
4. **Feature engineering** - MFCC yerine Mel-spectrogram veya her ikisini deneyin
5. **Ensemble yöntemleri** - Birden fazla modeli birleştirin

---

## 📝 Notlar

- Tüm modeller aynı özellik çıkarımını (MFCC) kullanır
- Her model aynı train/test split'i kullanır (random_state=42)
- Modeller pickle formatında kaydedilir
- Aynı anda birden fazla model yüklenebilir ve kullanılabilir

---

## 🔄 Sonraki Adımlar

- [ ] Hyperparameter tuning için GridSearchCV
- [ ] Cross-validation desteği
- [ ] Model ensemble yöntemleri
- [ ] Feature importance görselleştirme
- [ ] Model karşılaştırma raporları


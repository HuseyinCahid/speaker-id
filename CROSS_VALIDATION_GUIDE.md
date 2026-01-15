# 🔄 Cross-Validation ve Hyperparameter Tuning Rehberi

Bu dokümanda cross-validation ve hyperparameter tuning özelliklerinin nasıl kullanılacağı açıklanmaktadır.

## 📚 Temel Kavramlar

### Cross-Validation (Çapraz Doğrulama)
- Modelin genelleme performansını daha güvenilir şekilde ölçmek için kullanılır
- Veri setini k fold'a böler, her fold'u bir kez test seti olarak kullanır
- Overfitting'i tespit etmeye yardımcı olur

### Hyperparameter Tuning (Hiperparametre Ayarı)
- Modelin en iyi performansı göstermesi için optimal parametreleri bulur
- Grid Search: Tüm kombinasyonları dener (yavaş ama kapsamlı)
- Random Search: Rastgele kombinasyonları dener (hızlı ama daha az kapsamlı)

---

## 🚀 Kullanım

### 1. Sadece Cross-Validation

```bash
python train_model.py --model svm --cv --cv-folds 5
```

**Çıktı:**
```
🔄 Cross-Validation: ✅ (5 folds)
🔄 Performing 5-fold Cross-Validation...
   CV Mean Accuracy: 0.8750 (87.50%)
   CV Std: 0.0234 (2.34%)
   CV Scores: ['0.8500', '0.8800', '0.8700', '0.8900', '0.8850']
```

### 2. Sadece Hyperparameter Tuning

#### Grid Search (Tüm kombinasyonları dener)
```bash
python train_model.py --model svm --tune --tuning-method grid
```

#### Random Search (Rastgele kombinasyonlar)
```bash
python train_model.py --model svm --tune --tuning-method random --n-iter 20
```

**Çıktı:**
```
🎯 Hyperparameter Tuning: ✅ (grid)
🎯 Performing Hyperparameter Tuning (grid)...
   Searching through 3 parameter combinations...
   ✅ Best parameters found:
      C: 10
      gamma: 0.1
      kernel: rbf
   Best CV Score: 0.9125 (91.25%)
```

### 3. Her İkisini Birlikte

```bash
python train_model.py --model svm --cv --cv-folds 5 --tune --tuning-method grid
```

Bu durumda:
1. Önce cross-validation yapılır (basit model ile)
2. Sonra hyperparameter tuning yapılır (içinde kendi CV'si var)
3. En iyi model final test setinde değerlendirilir

---

## 📊 Model Bazında Hyperparameter Grid'leri

### SVM
```python
{
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
    'kernel': ['rbf', 'poly', 'sigmoid']
}
```

**Önerilen kullanım:**
- Küçük veri setleri: Grid Search
- Büyük veri setleri: Random Search (n_iter=30-50)

### Random Forest
```python
{
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
```

**Önerilen kullanım:**
- Random Search (çok fazla kombinasyon var)
- n_iter=50-100 önerilir

### Neural Network (MLP)
```python
{
    'hidden_layer_sizes': [(64,), (128,), (128, 64), (256, 128)],
    'alpha': [0.0001, 0.001, 0.01],
    'learning_rate_init': [0.0001, 0.001, 0.01],
    'activation': ['relu', 'tanh']
}
```

**Önerilen kullanım:**
- Random Search (eğitim uzun sürer)
- n_iter=20-30 yeterli

### AdaBoost
```python
{
    'n_estimators': [25, 50, 100],
    'learning_rate': [0.5, 1.0, 1.5, 2.0]
}
```

**Önerilen kullanım:**
- Grid Search (küçük grid)
- Hızlı sonuç verir

---

## 📝 Örnek Senaryolar

### Senaryo 1: Hızlı Test (SVM)
```bash
# Sadece CV ile hızlı değerlendirme
python train_model.py --model svm --cv --cv-folds 3
```

### Senaryo 2: Kapsamlı Optimizasyon (Random Forest)
```bash
# CV + Random Search
python train_model.py \
  --model random_forest \
  --cv --cv-folds 5 \
  --tune --tuning-method random \
  --n-iter 50
```

### Senaryo 3: Neural Network Optimizasyonu
```bash
# Random Search (Grid çok uzun sürer)
python train_model.py \
  --model neural_network \
  --tune --tuning-method random \
  --n-iter 30
```

### Senaryo 4: AdaBoost Hızlı Tuning
```bash
# Grid Search (küçük grid, hızlı)
python train_model.py \
  --model adaboost \
  --tune --tuning-method grid
```

---

## 📈 Metadata'da Saklanan Bilgiler

Eğer cross-validation veya tuning kullanılırsa, metadata dosyasına şu bilgiler eklenir:

### Cross-Validation Metadata
```json
{
  "cross_validation": {
    "cv_scores": [0.85, 0.88, 0.87, 0.89, 0.885],
    "cv_mean": 0.875,
    "cv_std": 0.0234,
    "cv_folds": 5
  }
}
```

### Hyperparameter Tuning Metadata
```json
{
  "best_hyperparameters": {
    "C": 10,
    "gamma": 0.1,
    "kernel": "rbf"
  },
  "hyperparameter_tuning_method": "grid"
}
```

---

## ⚡ Performans İpuçları

### 1. Veri Seti Boyutuna Göre Seçim

**Küçük Veri Seti (< 100 örnek):**
- ✅ Cross-validation kullanın (daha güvenilir metrikler)
- ✅ Grid Search (küçük grid'ler için hızlı)
- ⚠️ Random Search gereksiz (zaten az kombinasyon var)

**Orta Veri Seti (100-500 örnek):**
- ✅ Cross-validation (5 folds)
- ✅ Random Search (n_iter=20-30)

**Büyük Veri Seti (> 500 örnek):**
- ⚠️ Cross-validation yavaş olabilir (3 folds yeterli)
- ✅ Random Search (n_iter=50-100)

### 2. Model Tipine Göre Seçim

**SVM:**
- Grid Search genellikle hızlıdır
- Random Search da iyi çalışır

**Random Forest:**
- Random Search önerilir (çok fazla kombinasyon)
- Grid Search çok uzun sürebilir

**Neural Network:**
- Random Search önerilir (eğitim uzun sürer)
- Grid Search çok uzun sürebilir

**AdaBoost:**
- Grid Search hızlı ve yeterli

### 3. Zaman vs. Doğruluk Dengesi

**Hızlı Sonuç İstiyorsanız:**
```bash
--tune --tuning-method random --n-iter 10
```

**En İyi Sonuç İstiyorsanız:**
```bash
--tune --tuning-method grid
```

**Dengeli Yaklaşım:**
```bash
--tune --tuning-method random --n-iter 30
```

---

## 🔍 Sonuçları Yorumlama

### Cross-Validation Sonuçları

**İyi CV Sonuçları:**
- CV Mean: Yüksek (> 0.85)
- CV Std: Düşük (< 0.05)
- Tüm fold'lar benzer skorlar

**Kötü CV Sonuçları:**
- CV Mean: Düşük (< 0.70)
- CV Std: Yüksek (> 0.10)
- Fold'lar arasında büyük farklar

**Çözüm:**
- Daha fazla veri ekleyin
- Hyperparameter tuning yapın
- Farklı model deneyin

### Hyperparameter Tuning Sonuçları

**Başarılı Tuning:**
- Best CV Score > Train Accuracy (overfitting yok)
- Best CV Score > Test Accuracy (genelleme iyi)
- Parametreler makul aralıklarda

**Başarısız Tuning:**
- Best CV Score çok düşük
- Parametreler ekstrem değerlerde
- Grid yeterli değil

**Çözüm:**
- Grid'i genişletin
- Daha fazla iterasyon (Random Search)
- Farklı model deneyin

---

## 🐛 Sorun Giderme

### "Grid Search çok uzun sürüyor"

**Çözüm:**
- Random Search kullanın
- n_iter'i azaltın
- Grid'i küçültün (daha az parametre değeri)

### "CV skorları çok düşük"

**Çözüm:**
- Daha fazla veri ekleyin
- Hyperparameter tuning yapın
- Farklı model deneyin

### "Best parameters ekstrem değerlerde"

**Çözüm:**
- Grid'i genişletin
- Daha fazla veri ekleyin
- Model tipini değiştirin

---

## 📚 Ek Kaynaklar

- [scikit-learn Cross-Validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Grid Search vs Random Search](https://scikit-learn.org/stable/modules/grid_search.html)
- [Hyperparameter Tuning Best Practices](https://towardsdatascience.com/hyperparameter-tuning-c5619e8e6624)

---

## ✅ Özet

| Özellik | Komut | Ne Zaman Kullanılır |
|---------|-------|---------------------|
| Cross-Validation | `--cv --cv-folds 5` | Güvenilir performans metrikleri istediğinizde |
| Grid Search | `--tune --tuning-method grid` | Küçük grid'ler, hızlı modeller |
| Random Search | `--tune --tuning-method random --n-iter 20` | Büyük grid'ler, yavaş modeller |
| Her İkisi | `--cv --tune` | Kapsamlı optimizasyon |

**Önerilen Başlangıç:**
```bash
python train_model.py --model svm --cv --tune --tuning-method random --n-iter 20
```

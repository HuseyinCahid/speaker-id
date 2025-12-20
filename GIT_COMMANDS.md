# Git Push Komutları - HER ŞEYİ YÜKLE

Aşağıdaki komutları sırayla çalıştırın:

## 1. Git Status Kontrol
```bash
cd "C:\Users\varel\Desktop\Term Project 2\speaker-id"
git status
```

## 2. Tüm Dosyaları Ekle (data ve models dahil)
```bash
git add .
```

## 3. Commit Yap
```bash
git commit -m "Add complete speaker identification system with demo data

- Added FastAPI backend with audio processing
- Added Next.js frontend with RecordRTC audio recording
- Added web-based model training interface
- Implemented SVM model for speaker identification
- Added comprehensive documentation
- Fixed encoding issues for Windows
- Added multilingual support
- Included demo data and trained models"
```

## 4. GitHub'a Push Et
```bash
git push origin main
```

## Eğer Conflict Olursa

```bash
git pull origin main --no-rebase
# Çakışma varsa düzelt, sonra tekrar:
git add .
git commit -m "merge conflicts resolved"
git push origin main
```

## Eğer Force Push Gerekirse (DİKKATLI!)

```bash
git push origin main --force
```


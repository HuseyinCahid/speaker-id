# Web-Based Speaker Identification (COMP491-1)

Amaç:
Tarayıcıdan alınan kısa ses örneğiyle konuşmacıyı tanımak.
FastAPI backend (Python + Librosa + ML), Next.js frontend (TypeScript + Web Audio API).

## Proje Yapısı
- backend/  → FastAPI, model inference, Librosa ile feature extraction
- frontend/ → Next.js (mikrofon kaydı, dosya upload)
- data/
  - raw/        (ham ses, .wav - GIT'E PUSHLANMAZ)
  - processed/  (temizlenmiş / normalize ses - GIT'E PUSHLANMAZ)
- notebooks/ → MFCC çıkarma ve model eğitimi denemeleri
- docs/      → proje notları, rapor materyali

## Backend'i Çalıştırmak
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app:app --reload

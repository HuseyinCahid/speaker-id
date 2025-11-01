from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Speaker ID API",
    description="Konuşmacı tanıma servisi (FastAPI + Librosa + ML)",
    version="0.0.1"
)

# Basit sağlık kontrolü
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "backend is running"}

# İleride kullanacağımız tahmin endpoint iskeleti
@app.post("/predict")
async def predict_speaker(audio_file: UploadFile = File(...)):
    # Şimdilik sadece dosya bilgisini döndürüyoruz.
    # Sonraki adımlarda:
    # 1. WAV'i okuyacağız
    # 2. MFCC / Mel özellik çıkaracağız
    # 3. Modele vereceğiz
    # 4. speaker_id tahmini döneceğiz
    return JSONResponse({
        "filename": audio_file.filename,
        "detail": "Prediction endpoint stub - model henüz bağlı değil."
    })

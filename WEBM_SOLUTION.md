# WebM Format Sorunu - Çözüm

## Problem

Browser MediaRecorder WebM formatında kayıt yapıyor, ancak:
- Backend'deki Librosa WebM'i desteklemiyor
- FFmpeg gerekiyor ama Windows'ta kurulu değil
- Pydub FFmpeg gerektirir

## Çözüm 1: FFmpeg Kurulumu (Önerilen)

### Windows

1. FFmpeg'i indirin: https://ffmpeg.org/download.html
2. ZIP'i açın ve `ffmpeg.exe` dosyasını PATH'e ekleyin
3. Terminalde test edin: `ffmpeg -version`

FFmpeg kurulumdan sonra pydub ile WebM dönüşümü çalışacak.

## Çözüm 2: RecordRTC Kullan (Alternatif)

Frontend'de RecordRTC kütüphanesi kullanarak WAV formatında kayıt yap.

### Kurulum:

```bash
cd frontend
npm install recordrtc
```

### Kod Değişikliği:

AudioRecorder.tsx'de MediaRecorder yerine RecordRTC kullan.

## Çözüm 3: Geçici Çözüm (Şimdilik)

Eğitim sayfasından yükleyebilirsiniz (MP3/M4A dosyaları desteklenir).

## Hızlı Test

Backend'de test edin:

```python
from pydub import AudioSegment
audio = AudioSegment.from_file("test.webm", format="webm")
audio.export("output.wav", format="wav")
```

Eğer hata verirse, FFmpeg kurulu değildir.


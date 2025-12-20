Project Notes - Speaker ID

Audio collection standard:
- Sample rate: 16 kHz
- Channels: mono
- Clip duration: ~3 seconds per sample
- File format: WAV
- Naming: utt_0001.wav, utt_0002.wav, ...
- Label comes from folder name:
  data/raw/speaker_01/*.wav  -> label = "speaker_01"

Goal:
We'll later extract MFCC / Mel-spectrogram features with Librosa and train:
1) MFCC + SVM (scikit-learn)
2) Log-Mel + small CNN (PyTorch)
Then expose prediction through FastAPI (/predict).

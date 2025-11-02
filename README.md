# 🌐 Web-Based Real-Time Speech Recognition and Speaker Identification

## Description

This project modernizes earlier research on voice and speaker recognition by developing a web-based application capable of performing real-time speech recognition and speaker identification directly in the browser — without any cloud connection.

Using modern web technologies such as the Web Audio API, TensorFlow.js, and ONNX Runtime Web, the system will record, preprocess, and analyze audio locally on the client side.

This approach ensures low latency, data privacy, and cross-platform compatibility, making it suitable for use in education, authentication, and accessibility applications.

## Technical Stack

- **Backend**: FastAPI + Librosa + PyTorch (model training & inference)
- **Frontend**: Next.js + TypeScript + Web Audio API
- **On-Device ML**: TensorFlow.js / ONNX Runtime Web
- **Models**: x-vector, GhostNet, CNN-RNN hybrids
- **Features**: MFCC, Mel-spectrograms

## Project Structure

```
speaker-id/
├── backend/          # FastAPI server, model inference, feature extraction
├── frontend/         # Next.js app (microphone recording, visualization)
├── notebooks/        # Jupyter notebooks (model training experiments)
├── models/           # Trained models (ONNX, TensorFlow.js)
├── data/             # Audio datasets (NOT pushed to git)
│   ├── raw/          # Raw audio files (.wav)
│   └── processed/    # Preprocessed features
└── docs/             # Project notes, reports

```

## Research Goals

**What is the optimal balance between model accuracy and real-time performance (latency) for a web-based speaker identification system using different quantization levels and architectures?**

## Implementation Roadmap

### ✅ Phase 1: Project Setup & Backend Infrastructure
- [x] Clone repository
- [x] Create project structure
- [x] Backend API endpoints
- [x] Audio processing pipeline

### ✅ Phase 2: Frontend Development
- [x] Next.js frontend setup
- [x] Web Audio API integration
- [x] Real-time audio recording
- [x] UI/UX design

### 🔄 Phase 3: Model Development (Offline)
- [ ] Dataset collection (VoxCeleb/LibriSpeech)
- [ ] Feature extraction (MFCC, Mel-spectrograms)
- [ ] Train speaker ID model (x-vector/GhostResNet)
- [ ] Model evaluation & testing
- [ ] Model conversion (TensorFlow.js/ONNX)

### ⚡ Phase 4: Optimization
- [ ] Model quantization (float32, float16, int8)
- [ ] Browser performance testing
- [ ] Latency profiling

### 📊 Phase 5: Evaluation & Analysis
- [ ] Cross-browser testing
- [ ] Device compatibility tests
- [ ] Accuracy vs. latency analysis
- [ ] Documentation & report

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Expected Outcomes

- Fully functional web prototype with real-time speaker identification
- Performance evaluation across quantization levels and model types
- Applications: e-learning, voice authentication, accessibility tools

## References

- VoxCeleb Dataset
- LibriSpeech Dataset
- TensorFlow.js Documentation
- ONNX Runtime Web

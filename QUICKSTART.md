# Quick Start Guide

## Prerequisites

- Python 3.9+ with pip
- Node.js 18+ with npm
- Git

## Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload
```

The backend API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Testing the Application

1. Make sure both backend and frontend servers are running
2. Open `http://localhost:3000` in your browser
3. Click the microphone button to start recording
4. Speak for a few seconds
5. Click the stop button
6. The audio will be sent to the backend for prediction

## Model Training

### Basic Training
```bash
# Train SVM model (default)
python train_model.py

# Train specific model type
python train_model.py --model random_forest
python train_model.py --model neural_network
python train_model.py --model adaboost
```

### With Cross-Validation
```bash
# 5-fold cross-validation
python train_model.py --model svm --cv --cv-folds 5

# 3-fold cross-validation (faster)
python train_model.py --model svm --cv --cv-folds 3
```

### With Hyperparameter Tuning
```bash
# Grid Search (comprehensive but slower)
python train_model.py --model svm --tune --tuning-method grid

# Random Search (faster, good for large grids)
python train_model.py --model svm --tune --tuning-method random --n-iter 20
```

### Combined (Recommended)
```bash
# Cross-validation + Hyperparameter tuning
python train_model.py --model svm --cv --cv-folds 5 --tune --tuning-method random --n-iter 20
```

**See `CROSS_VALIDATION_GUIDE.md` for detailed usage.**

## Current Status

✅ **Completed:**
- Project structure
- Backend API with audio processing
- Frontend UI with Web Audio API
- MFCC feature extraction
- Model training with multiple algorithms (SVM, Random Forest, Neural Network, AdaBoost)
- **Cross-validation support** 🆕
- **Hyperparameter tuning (Grid Search & Random Search)** 🆕
- Web-based model training interface
- Model analytics and visualization

🚧 **In Progress:**
- Model deployment optimization
- Browser-side inference

📋 **Next Steps:**
1. Collect/download audio dataset
2. Train models with cross-validation and tuning
3. Deploy optimized models to backend
4. Optimize for browser deployment

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Change port
uvicorn app:app --reload --port 8001
```

### Frontend Issues

**Module not found:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Make sure backend is running on port 8000
- Check backend allows CORS (already configured)

## API Endpoints

### GET /
Root endpoint with API information

### GET /health
Health check and status information

### GET /models
List loaded models and speakers

### POST /predict
Predict speaker from audio file

**Parameters:**
- `audio_file`: Audio file (WAV/WebM)
- `feature_type`: 'mfcc' or 'mel' (default: 'mfcc')
- `top_k`: Number of top predictions (default: 3)

**Example:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "audio_file=@test.wav" \
  -F "feature_type=mfcc" \
  -F "top_k=3"
```

### POST /audio-stats
Get statistics about audio file

**Parameters:**
- `audio_file`: Audio file

## Development

### Adding New Features

1. Backend features: Edit files in `backend/`
2. Frontend features: Edit files in `frontend/app/`
3. Model development: Use Jupyter notebooks in `notebooks/`

### Code Structure

```
speaker-id/
├── backend/          # FastAPI application
│   ├── app.py       # Main API endpoints
│   ├── audio_processor.py  # Audio processing
│   └── model_manager.py    # Model management
├── frontend/         # Next.js application
│   └── app/
│       ├── page.tsx  # Main page
│       └── components/  # React components
├── notebooks/        # Jupyter notebooks
├── models/           # Trained models
└── data/             # Audio datasets (gitignored)
```

## Next Steps

See `docs/project_plan.md` for detailed roadmap and implementation plan.


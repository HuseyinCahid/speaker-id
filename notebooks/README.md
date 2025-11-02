# Notebooks Directory

This directory contains Jupyter notebooks for model development and experimentation.

## Notebooks

1. **01_feature_extraction.ipynb** - Feature extraction from audio files
   - Load audio files
   - Extract MFCC features
   - Extract Mel-spectrograms
   - Visualize features
   - Batch process dataset

2. **02_model_training.ipynb** - Model training and evaluation
   - SVM classifier training
   - CNN model training
   - Model evaluation
   - Model saving

## Setup

```bash
# Install Jupyter
pip install jupyter ipykernel

# Install notebook dependencies
pip install -r ../backend/requirements.txt
pip install scikit-learn torch torchaudio matplotlib

# Start Jupyter
jupyter notebook
```

## Usage

1. Start with `01_feature_extraction.ipynb` to extract features from your audio dataset
2. Run `02_model_training.ipynb` to train and evaluate models
3. Models will be saved to `../models/` directory

## Dataset Structure

```
data/
└── raw/
    ├── speaker_01/
    │   ├── utt_0001.wav
    │   ├── utt_0002.wav
    │   └── ...
    ├── speaker_02/
    │   ├── utt_0001.wav
    │   └── ...
    └── ...
```


'use client';

import { useState } from 'react';
import AudioRecorder from './components/AudioRecorder';
import PredictionResult from './components/PredictionResult';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAudioRecorded = async (audioBlob: Blob) => {
    setLoading(true);
    setError(null);
    
    try {
      // Convert blob to File for FormData
      const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
      
      // Create FormData
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      formData.append('feature_type', 'mfcc');
      formData.append('top_k', '3');

      // Send to backend
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = 'Failed to process audio';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setResult(data);
      
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
      setResult({ error: err instanceof Error ? err.message : 'An error occurred' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Speaker Identification
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Real-time speaker identification using Web Audio API and Machine Learning
          </p>
        </div>

        {/* Main content */}
        <div className="flex flex-col items-center gap-8">
          {/* Audio Recorder */}
          <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
              Record Audio
            </h2>
            <AudioRecorder onAudioRecorded={handleAudioRecorded} />
          </div>

          {/* Error message */}
          {error && (
            <div className="w-full max-w-2xl bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-center">{error}</p>
            </div>
          )}

          {/* Prediction Result */}
          <PredictionResult result={result} loading={loading} />
        </div>

        {/* Info section */}
        <div className="mt-16 text-center">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="font-bold mb-2">Privacy First</h3>
              <p className="text-sm text-gray-600">
                All processing happens on your device. No cloud connection required.
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="font-bold mb-2">Real-Time</h3>
              <p className="text-sm text-gray-600">
                Instant speaker identification with low latency processing.
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="font-bold mb-2">Accurate</h3>
              <p className="text-sm text-gray-600">
                Powered by state-of-the-art ML models for high accuracy.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center space-y-4">
          <div>
            <a
              href="/train"
              className="inline-block bg-gradient-to-r from-green-600 to-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:from-green-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              🎓 Model Eğit
            </a>
          </div>
          <p className="text-gray-500 text-sm">
            Web-Based Speaker Identification System
            {' • '}
            <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline">
              API Documentation
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

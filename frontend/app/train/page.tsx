'use client';

import { useState } from 'react';

export default function TrainPage() {
  const [speakerName, setSpeakerName] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingResult, setTrainingResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const files = Array.from(event.target.files);
      setSelectedFiles(prev => [...prev, ...files]);
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleTrain = async () => {
    if (!speakerName.trim()) {
      setError('Please enter a speaker name');
      return;
    }

    if (selectedFiles.length < 3) {
      setError('Please add at least 3 audio files per speaker');
      return;
    }

    setIsTraining(true);
    setError(null);
    setTrainingResult(null);

    try {
      // Upload audio files
      const formData = new FormData();
      formData.append('speaker_name', speakerName);
      
      selectedFiles.forEach((file, index) => {
        formData.append(`audio_files`, file);
      });

      const response = await fetch('http://localhost:8000/train', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Training failed');
      }

      const result = await response.json();
      setTrainingResult(result);

      // Clear form
      setSpeakerName('');
      setSelectedFiles([]);

    } catch (err) {
      console.error('Training error:', err);
      setError(err instanceof Error ? err.message : 'Training failed');
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
            Model Eğitimi
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Ses kayıtlarını yükleyin ve konuşmacı tanıma modelini eğitin
          </p>
        </div>

        {/* Training Form */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200 mb-8">
          {/* Speaker Name Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Konuşmacı Adı
            </label>
            <input
              type="text"
              value={speakerName}
              onChange={(e) => setSpeakerName(e.target.value)}
              placeholder="Örn: speaker_01, Ahmet, Maria..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isTraining}
            />
            <p className="mt-1 text-sm text-gray-500">
              Her konuşmacı için benzersiz bir isim girin
            </p>
          </div>

          {/* File Upload */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ses Dosyaları
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-green-500 transition-colors">
              <input
                type="file"
                accept="audio/*"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
                disabled={isTraining}
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer"
              >
                <div className="text-4xl mb-2">📁</div>
                <p className="text-gray-600 mb-2">
                  Dosyaları seçmek için tıklayın veya sürükleyin
                </p>
                <p className="text-sm text-gray-500">
                  WAV, MP3, M4A formatları desteklenir
                </p>
              </label>
            </div>

            {/* Selected Files List */}
            {selectedFiles.length > 0 && (
              <div className="mt-4 space-y-2">
                <p className="text-sm font-medium text-gray-700">
                  Seçilen Dosyalar ({selectedFiles.length}):
                </p>
                {selectedFiles.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between bg-gray-50 rounded-lg p-3"
                  >
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl">🎵</span>
                      <div>
                        <p className="text-sm font-medium text-gray-800">
                          {file.name}
                        </p>
                        <p className="text-xs text-gray-500">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                    </div>
                    {!isTraining && (
                      <button
                        onClick={() => removeFile(index)}
                        className="text-red-600 hover:text-red-800 text-xl"
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-center">{error}</p>
            </div>
          )}

          {/* Train Button */}
          <button
            onClick={handleTrain}
            disabled={isTraining || selectedFiles.length < 3 || !speakerName.trim()}
            className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
              isTraining || selectedFiles.length < 3 || !speakerName.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-green-600 to-blue-600 text-white hover:from-green-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:scale-[1.02]'
            }`}
          >
            {isTraining ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin mr-2">⏳</span>
                Model Eğitiliyor...
              </span>
            ) : (
              '🎓 Modeli Eğit'
            )}
          </button>
        </div>

        {/* Training Result */}
        {trainingResult && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-green-800 mb-4">
              ✅ Eğitim Tamamlandı!
            </h2>
            <div className="space-y-3">
              <p className="text-gray-700">
                <span className="font-semibold">Konuşmacı:</span>{' '}
                {trainingResult.speaker_name}
              </p>
              <p className="text-gray-700">
                <span className="font-semibold">Eklenen Dosya:</span>{' '}
                {trainingResult.files_added}
              </p>
              <p className="text-gray-700">
                <span className="font-semibold">Model Doğruluğu:</span>{' '}
                <span className="text-green-600 font-bold">
                  {(trainingResult.accuracy * 100).toFixed(1)}%
                </span>
              </p>
            </div>
          </div>
        )}

        {/* Info Section */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6 border border-blue-200">
          <h3 className="text-xl font-bold mb-4 text-blue-900">
            💡 İpuçları
          </h3>
          <ul className="space-y-2 text-gray-700">
            <li>⚠️ <strong>ÖNEMLİ: En az 2 farklı konuşmacı eklemeniz gerekir!</strong></li>
            <li>✅ Her konuşmacı için en az 5-10 ses kaydı ekleyin</li>
            <li>✅ 3-5 saniyelik kayıtlar ideal uzunluktadır</li>
            <li>✅ Sessiz ortamlarda kayıt yapın</li>
            <li>✅ Her kayıt için farklı ifadeler kullanın</li>
            <li>✅ İlk konuşmacıdan sonra diğerlerini ekleyin</li>
          </ul>
        </div>

        {/* Back Link */}
        <div className="mt-8 text-center">
          <a
            href="/"
            className="text-blue-600 hover:text-blue-800 underline"
          >
            ← Ana Sayfaya Dön
          </a>
        </div>
      </div>
    </div>
  );
}


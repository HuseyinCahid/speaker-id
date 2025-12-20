'use client';

import { useState } from 'react';
import AudioRecorder from './components/AudioRecorder';
import PredictionResult from './components/PredictionResult';

type ApiPrediction = {
  filename: string;
  feature_type: string;
  prediction: {
    top1: { label: string; prob: number };
    topk?: Array<{ label: string; prob: number }>;
  };
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

export default function Home() {
  // Common states
  const [result, setResult] = useState<ApiPrediction | any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Single file test states
  const [testFile, setTestFile] = useState<File | null>(null);
  const [topk, setTopk] = useState<number>(3);

  // Batch test states
  const [batchFiles, setBatchFiles] = useState<FileList | null>(null);
  const [expectedLabel, setExpectedLabel] = useState<string>('');
  const [batchRunning, setBatchRunning] = useState(false);
  const [batchLog, setBatchLog] = useState<string[]>([]);
  const [batchSummary, setBatchSummary] = useState<{ ok: number; total: number; acc: number } | null>(null);

  // === Existing: record & send ===
  const handleAudioRecorded = async (audioBlob: Blob) => {
    setLoading(true);
    setError(null);
    try {
      const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      formData.append('feature_type', 'mfcc'); // Always use MFCC
      formData.append('top_k', String(topk));

      const response = await fetch(`${API_BASE}/predict`, { method: 'POST', body: formData });
      if (!response.ok) {
        let msg = 'Failed to process audio';
        try {
          const e = await response.json();
          msg = e.detail || msg;
        } catch {
          msg = response.statusText || msg;
        }
        throw new Error(msg);
      }

      const data = (await response.json()) as ApiPrediction;
      setResult(data);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
      setResult({ error: err instanceof Error ? err.message : 'An error occurred' });
    } finally {
      setLoading(false);
    }
  };

  // === New: single file upload test ===
  const handleSingleFileTest = async () => {
    if (!testFile) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const fd = new FormData();
      fd.append('audio_file', testFile);
      fd.append('feature_type', 'mfcc'); // Always use MFCC
      fd.append('top_k', String(topk));

      const r = await fetch(`${API_BASE}/predict`, { method: 'POST', body: fd });
      if (!r.ok) {
        let msg = 'Upload failed';
        try {
          const e = await r.json();
          msg = e.detail || msg;
        } catch {
          msg = r.statusText || msg;
        }
        throw new Error(msg);
      }
      const data = (await r.json()) as ApiPrediction;
      setResult(data);
    } catch (e: any) {
      setError(e?.message ?? 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  // === New: batch test (multiple files for one expected label) ===
  const runBatchTest = async () => {
    if (!batchFiles || !expectedLabel.trim()) return;
    setBatchRunning(true);
    setBatchLog([]);
    setBatchSummary(null);
    let ok = 0, total = 0;

    for (const f of Array.from(batchFiles)) {
      const fd = new FormData();
      fd.append('audio_file', f);
      fd.append('feature_type', 'mfcc'); // Always use MFCC
      fd.append('top_k', String(topk));

      try {
        const r = await fetch(`${API_BASE}/predict`, { method: 'POST', body: fd });
        const data = (await r.json()) as ApiPrediction;
        const pred = data?.prediction?.top1?.label ?? 'NA';
        total += 1;
        ok += pred === expectedLabel ? 1 : 0;
        setBatchLog(prev => [...prev, `${f.name} -> ${pred} (${pred === expectedLabel ? '✓' : '✗'})`]);
      } catch {
        total += 1;
        setBatchLog(prev => [...prev, `${f.name} -> ERROR`]);
      }

      // küçük bir nefes
      await new Promise(res => setTimeout(res, 100));
    }

    setBatchSummary({ ok, total, acc: total ? ok / total : 0 });
    setBatchRunning(false);
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
            Record or upload audio and get real-time speaker predictions
          </p>
        </div>

        {/* TopK control */}
        <div className="flex flex-wrap justify-center items-center gap-4 mb-6">
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-700">Top-K:</label>
            <input
              type="number"
              value={topk}
              min={1}
              max={5}
              onChange={(e) => setTopk(Number(e.target.value))}
              className="w-20 border px-2 py-1 rounded"
            />
          </div>
          <div className="text-sm text-gray-600">
            Özellik Tipi: <span className="font-semibold">MFCC</span> (varsayılan)
          </div>
        </div>

        {/* Main content */}
        <div className="flex flex-col items-center gap-8">
          {/* Audio Recorder */}
          <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
              Record Audio
            </h2>
            <AudioRecorder
  onAudioRecorded={handleAudioRecorded}  
  
/>
          </div>

          {/* Single File Test */}
          <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
              Dosyadan Test (Tek Dosya)
            </h2>
            <div className="flex flex-col gap-3">
              <input
                type="file"
                accept=".wav,.mp3,.m4a,.ogg,.webm"
                onChange={(e) => setTestFile(e.target.files?.[0] ?? null)}
              />
              <button
                onClick={handleSingleFileTest}
                disabled={!testFile || loading}
                className="px-4 py-2 rounded bg-blue-600 text-white disabled:opacity-50"
              >
                {loading ? 'Yükleniyor...' : 'Modeli Test Et'}
              </button>
            </div>
          </div>

          {/* Batch Test */}
          <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
              Toplu Test (Batch) – Accuracy Ölç
            </h2>
            <div className="flex flex-col gap-4">
              <input
                type="file"
                multiple
                accept=".wav,.mp3,.m4a,.ogg,.webm"
                onChange={(e) => setBatchFiles(e.target.files)}
              />
              <div className="flex items-center gap-2">
                <label className="text-sm text-gray-700">Beklenen etiket (konuşmacı adı):</label>
                <input
                  className="border px-2 py-1 rounded flex-1"
                  placeholder="ör. Huseyin / Cem Say"
                  value={expectedLabel}
                  onChange={(e) => setExpectedLabel(e.target.value)}
                />
              </div>
              <button
                onClick={runBatchTest}
                disabled={!batchFiles || !expectedLabel || batchRunning}
                className="px-4 py-2 rounded bg-emerald-600 text-white disabled:opacity-50"
              >
                {batchRunning ? 'Çalışıyor...' : 'Batch Testi Başlat'}
              </button>

              {batchSummary && (
                <div className="bg-emerald-50 border border-emerald-200 rounded p-3">
                  <b>Top-1 Accuracy:</b>{' '}
                  {batchSummary.ok}/{batchSummary.total} = {(batchSummary.acc * 100).toFixed(1)}%
                </div>
              )}

              <div className="max-h-48 overflow-auto bg-gray-50 p-2 text-sm rounded">
                {batchLog.map((l, i) => (
                  <div key={i}>{l}</div>
                ))}
              </div>
            </div>
          </div>

          {/* Error message */}
          {error && (
            <div className="w-full max-w-2xl bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-center">{error}</p>
            </div>
          )}

          {/* Prediction Result */}
          <PredictionResult result={result} loading={loading || batchRunning} />
        </div>

        {/* Info section */}
        <div className="mt-16 text-center">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="font-bold mb-2">Gizlilik</h3>
              <p className="text-sm text-gray-600">
                Ses dosyanız yerel backend’e gönderilip işlenir. Demo aşamasında bulut kullanılmaz.
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="font-bold mb-2">Gerçek Zamanlı</h3>
              <p className="text-sm text-gray-600">
                Düşük gecikmeli önişleme ve tahmin ile anlık sonuçlar.
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="font-bold mb-2">Ölçülebilir</h3>
              <p className="text-sm text-gray-600">
                Tek dosya veya toplu test ile doğruluğu metriklerle gözlemleyin.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center space-y-4">
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="/train"
              className="inline-block bg-gradient-to-r from-green-600 to-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:from-green-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              🎓 Model Eğit
            </a>
            <a
              href="/analytics"
              className="inline-block bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              📊 Model Analitikleri
            </a>
          </div>
          <p className="text-gray-500 text-sm">
            Web-Based Speaker Identification System
            {' • '}
            <a href={`${API_BASE}/docs`} className="text-blue-600 hover:underline">
              API Documentation
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

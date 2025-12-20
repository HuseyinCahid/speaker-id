'use client';

import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

interface ModelMetrics {
  model_type: string;
  test_accuracy: number;
  train_accuracy: number;
  precision_macro: number;
  recall_macro: number;
  f1_macro: number;
  precision_weighted: number;
  recall_weighted: number;
  f1_weighted: number;
  num_speakers: number;
  confusion_matrix: number[][];
  speakers: string[];
}

interface MetricsData {
  models: Record<string, ModelMetrics>;
  best_model: string | null;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch(`${API_BASE}/metrics`);
      if (!response.ok) {
        throw new Error('Failed to fetch metrics');
      }
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load metrics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-800 mb-4">Hata</h2>
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchMetrics}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!metrics || Object.keys(metrics.models).length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 max-w-md text-center">
          <h2 className="text-2xl font-bold text-yellow-800 mb-4">Model Bulunamadı</h2>
          <p className="text-yellow-600 mb-4">
            Görselleştirme için önce bir model eğitmeniz gerekiyor.
          </p>
          <a
            href="/train"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Model Eğit
          </a>
        </div>
      </div>
    );
  }

  // Model karşılaştırma verilerini hazırla
  const modelComparison = Object.entries(metrics.models).map(([name, data]) => ({
    name: data.model_type?.toUpperCase() || name.replace('_speaker_model.pkl', ''),
    accuracy: (data.test_accuracy * 100).toFixed(1),
    precision: (data.precision_macro * 100).toFixed(1),
    recall: (data.recall_macro * 100).toFixed(1),
    f1: (data.f1_macro * 100).toFixed(1),
  }));

  // Radar chart için veri
  const radarData = Object.entries(metrics.models).map(([name, data]) => ({
    model: data.model_type?.toUpperCase() || name.replace('_speaker_model.pkl', ''),
    Accuracy: data.test_accuracy * 100,
    Precision: data.precision_macro * 100,
    Recall: data.recall_macro * 100,
    'F1-Score': data.f1_macro * 100,
  }));

  // En iyi modelin confusion matrix'i
  const bestModelData = metrics.best_model ? metrics.models[metrics.best_model] : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Model Analitikleri
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Model performans metrikleri ve görselleştirmeleri
          </p>
        </div>

        {/* Best Model Info */}
        {metrics.best_model && (
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 mb-8 text-white shadow-lg">
            <h2 className="text-2xl font-bold mb-2">🏆 En İyi Model</h2>
            <p className="text-lg">
              {bestModelData?.model_type?.toUpperCase() || metrics.best_model.replace('_speaker_model.pkl', '')}
              {' '}
              - Test Accuracy: {(bestModelData?.test_accuracy || 0) * 100}%
            </p>
          </div>
        )}

        {/* Model Comparison Chart */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Model Karşılaştırması</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={modelComparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis label={{ value: 'Yüzde (%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value: string) => `${value}%`} />
              <Legend />
              <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy" />
              <Bar dataKey="precision" fill="#10b981" name="Precision" />
              <Bar dataKey="recall" fill="#f59e0b" name="Recall" />
              <Bar dataKey="f1" fill="#ef4444" name="F1-Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Chart */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Performans Radar Grafiği</h2>
          <ResponsiveContainer width="100%" height={500}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="model" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar
                name="Accuracy"
                dataKey="Accuracy"
                stroke="#3b82f6"
                fill="#3b82f6"
                fillOpacity={0.6}
              />
              <Radar
                name="Precision"
                dataKey="Precision"
                stroke="#10b981"
                fill="#10b981"
                fillOpacity={0.6}
              />
              <Radar
                name="Recall"
                dataKey="Recall"
                stroke="#f59e0b"
                fill="#f59e0b"
                fillOpacity={0.6}
              />
              <Radar
                name="F1-Score"
                dataKey="F1-Score"
                stroke="#ef4444"
                fill="#ef4444"
                fillOpacity={0.6}
              />
              <Legend />
              <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Accuracy Comparison Line Chart */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Train vs Test Accuracy</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={Object.entries(metrics.models).map(([name, data]) => ({
              name: data.model_type?.toUpperCase() || name.replace('_speaker_model.pkl', ''),
              'Train Accuracy': (data.train_accuracy * 100).toFixed(1),
              'Test Accuracy': (data.test_accuracy * 100).toFixed(1),
            }))}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value: string) => `${value}%`} />
              <Legend />
              <Line type="monotone" dataKey="Train Accuracy" stroke="#8b5cf6" strokeWidth={2} />
              <Line type="monotone" dataKey="Test Accuracy" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Detailed Metrics Table */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Detaylı Metrikler</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Model
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Test Accuracy
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Precision
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Recall
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    F1-Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Konuşmacı Sayısı
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(metrics.models).map(([name, data]) => (
                  <tr
                    key={name}
                    className={metrics.best_model === name ? 'bg-green-50' : ''}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className="text-sm font-medium text-gray-900">
                          {data.model_type?.toUpperCase() || name.replace('_speaker_model.pkl', '')}
                        </span>
                        {metrics.best_model === name && (
                          <span className="ml-2 text-xs bg-green-500 text-white px-2 py-1 rounded">
                            BEST
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {(data.test_accuracy * 100).toFixed(2)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {(data.precision_macro * 100).toFixed(2)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {(data.recall_macro * 100).toFixed(2)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {(data.f1_macro * 100).toFixed(2)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.num_speakers}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Confusion Matrix for Best Model */}
        {bestModelData && bestModelData.confusion_matrix && (
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              Confusion Matrix - {bestModelData.model_type?.toUpperCase()}
            </h2>
            <div className="overflow-x-auto">
              <table className="min-w-full border-collapse border border-gray-300">
                <thead>
                  <tr>
                    <th className="border border-gray-300 px-4 py-2 bg-gray-100"></th>
                    {bestModelData.speakers.map((speaker, idx) => (
                      <th key={idx} className="border border-gray-300 px-4 py-2 bg-gray-100 text-xs">
                        Pred: {speaker.length > 15 ? speaker.substring(0, 15) + '...' : speaker}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {bestModelData.confusion_matrix.map((row, rowIdx) => (
                    <tr key={rowIdx}>
                      <td className="border border-gray-300 px-4 py-2 bg-gray-100 text-xs font-medium">
                        Actual: {bestModelData.speakers[rowIdx]?.length > 15 
                          ? bestModelData.speakers[rowIdx].substring(0, 15) + '...' 
                          : bestModelData.speakers[rowIdx]}
                      </td>
                      {row.map((cell, colIdx) => (
                        <td
                          key={colIdx}
                          className={`border border-gray-300 px-4 py-2 text-center ${
                            rowIdx === colIdx
                              ? 'bg-green-100 font-bold'
                              : cell > 0
                              ? 'bg-red-100'
                              : 'bg-white'
                          }`}
                        >
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-4 text-sm text-gray-600">
              <span className="inline-block w-4 h-4 bg-green-100 mr-2"></span>
              Doğru tahminler (diagonal)
              <span className="inline-block w-4 h-4 bg-red-100 mr-2 ml-4"></span>
              Yanlış tahminler
            </p>
          </div>
        )}

        {/* Back Link */}
        <div className="text-center mt-8">
          <a
            href="/"
            className="text-blue-600 hover:text-blue-800 underline text-lg"
          >
            ← Ana Sayfaya Dön
          </a>
        </div>
      </div>
    </div>
  );
}


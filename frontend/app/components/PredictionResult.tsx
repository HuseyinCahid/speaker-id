'use client';

interface Speaker {
  speaker_id: string;
  confidence: number;
  speaker_name: string;
}

interface PredictionResultProps {
  result: {
    filename?: string;
    feature_type?: string;
    audio_stats?: {
      duration_ms: number;
      sample_rate: number;
      mean: number;
      std: number;
    };
    features_shape?: number[];
    prediction?: {
      model_used?: string;
      predictions?: Speaker[];
      timestamp_ms?: number;
    };
    error?: string;
  };
  loading?: boolean;
}

export default function PredictionResult({ result, loading }: PredictionResultProps) {
  if (loading) {
    return (
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-8 border border-gray-200">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/2" />
          <div className="h-4 bg-gray-200 rounded w-3/4" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
        </div>
      </div>
    );
  }

  if (!result || Object.keys(result).length === 0) {
    return (
      <div className="w-full max-w-2xl bg-gray-50 rounded-lg p-8 border border-gray-200">
        <p className="text-center text-gray-500">No prediction yet. Record audio to get started.</p>
      </div>
    );
  }

  if (result.error) {
    return (
      <div className="w-full max-w-2xl bg-red-50 rounded-lg shadow-lg p-8 border border-red-200">
        <h2 className="text-2xl font-bold text-red-800 mb-4">Error</h2>
        <p className="text-red-600">{result.error}</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-8 border border-gray-200">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Prediction Result</h2>
      
      {/* Metadata */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2 text-gray-700">Audio Information</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Filename:</span>
            <span className="ml-2 font-mono text-gray-800">{result.filename || 'N/A'}</span>
          </div>
          <div>
            <span className="text-gray-600">Duration:</span>
            <span className="ml-2 font-mono text-gray-800">
              {result.audio_stats?.duration_ms?.toFixed(0)} ms
            </span>
          </div>
          <div>
            <span className="text-gray-600">Sample Rate:</span>
            <span className="ml-2 font-mono text-gray-800">
              {result.audio_stats?.sample_rate || 'N/A'} Hz
            </span>
          </div>
          <div>
            <span className="text-gray-600">Feature Type:</span>
            <span className="ml-2 font-mono text-gray-800">{result.feature_type || 'N/A'}</span>
          </div>
        </div>
      </div>

      {/* Predictions */}
      {result.prediction?.predictions && result.prediction.predictions.length > 0 && (
        <div>
          <h3 className="font-semibold mb-4 text-gray-700">Top Predictions</h3>
          <div className="space-y-3">
            {result.prediction.predictions.map((speaker, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-2 transition-all ${
                  index === 0
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-lg text-gray-800">
                    {index === 0 && '🏆 '}
                    {speaker.speaker_name || speaker.speaker_id}
                  </span>
                  <span className="text-sm font-mono text-gray-600">
                    {(speaker.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                {/* Confidence bar */}
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      index === 0 ? 'bg-blue-600' : 'bg-gray-400'
                    }`}
                    style={{ width: `${speaker.confidence * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Model info */}
      {result.prediction?.model_used && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            Model: <span className="font-mono">{result.prediction.model_used}</span>
          </p>
        </div>
      )}
    </div>
  );
}


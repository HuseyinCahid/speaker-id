'use client';

import { useState, useRef, useEffect } from 'react';

interface AudioRecorderProps {
  onAudioRecorded: (audioBlob: Blob) => void;
}

export default function AudioRecorder({ onAudioRecorded }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [volume, setVolume] = useState(0);

  const RecordRTCRef = useRef<any>(null);
  const recorderRef = useRef<any>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const startTimeRef = useRef<number | null>(null);

  // Dynamically import RecordRTC on client side
  useEffect(() => {
    if (typeof window !== 'undefined') {
      import('recordrtc').then((RecordRTCModule) => {
        RecordRTCRef.current = RecordRTCModule.default;
      });
    }
  }, []);

  // Start recording
  const startRecording = async () => {
    try {
      if (!RecordRTCRef.current) {
        setError('Recording library not loaded yet');
        return;
      }

      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
        } 
      });
      
      streamRef.current = stream;

      // Set up audio context for volume visualization
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256;
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);

      // Set up RecordRTC for WAV recording
      const recorder = new RecordRTCRef.current(stream, {
        type: 'audio',
        mimeType: 'audio/wav',
        sampleRate: 16000,
        numberOfAudioChannels: 1,
        recorderType: RecordRTCRef.current.StereoAudioRecorder,
      });

      recorderRef.current = recorder;

      // Start recording
      recorder.startRecording();
      setIsRecording(true);
      startTimeRef.current = Date.now();

      // Start volume monitoring
      monitorVolume();
      
    } catch (err) {
      console.error('Error starting recording:', err);
      setError('Failed to access microphone. Please check permissions.');
      setIsRecording(false);
    }
  };

  // Monitor audio volume for visualization
  const monitorVolume = () => {
    const analyser = analyserRef.current;
    if (!analyser) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const checkVolume = () => {
      if (isRecording && analyser) {
        analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((sum, val) => sum + val, 0) / bufferLength;
        setVolume(average);
        animationFrameRef.current = requestAnimationFrame(checkVolume);
      }
    };

    checkVolume();
  };

  // Stop recording
  const stopRecording = () => {
    if (recorderRef.current && isRecording) {
      recorderRef.current.stopRecording(() => {
        const blob = recorderRef.current?.getBlob();
        if (blob) {
          onAudioRecorded(blob);
        }
        
        // Cleanup
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
        }
        if (audioContextRef.current) {
          audioContextRef.current.close();
        }
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        if (recorderRef.current) {
          recorderRef.current.destroy();
        }
      });
      
      setIsRecording(false);
      setRecordingDuration(0);
      setVolume(0);
      
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    }
  };

  // Update recording duration
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (isRecording) {
      interval = setInterval(() => {
        if (startTimeRef.current) {
          const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
          setRecordingDuration(elapsed);
        }
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (recorderRef.current) {
        recorderRef.current.destroy();
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center gap-6">
      <div className="relative w-64 h-64 flex items-center justify-center">
        {/* Volume visualization circle */}
        <div className="absolute inset-0 rounded-full border-8 border-blue-200" />
        <div 
          className="absolute inset-0 rounded-full border-8 border-blue-600 transition-all duration-100"
          style={{ 
            opacity: volume / 100,
            transform: `scale(${1 + volume / 500})`
          }}
        />
        
        {/* Central button */}
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!!error}
          className={`
            relative z-10 w-24 h-24 rounded-full font-bold text-lg
            transition-all duration-300 shadow-lg
            ${isRecording 
              ? 'bg-red-600 hover:bg-red-700 animate-pulse' 
              : 'bg-blue-600 hover:bg-blue-700'
            }
            ${error ? 'opacity-50 cursor-not-allowed' : 'hover:scale-110'}
          `}
        >
          {isRecording ? '⏹' : '🎤'}
        </button>
      </div>

      {/* Status text */}
      <div className="text-center">
        {error && (
          <p className="text-red-600 mb-2">{error}</p>
        )}
        {!error && (
          <>
            <p className="text-lg font-medium">
              {isRecording ? 'Recording...' : 'Ready to Record'}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              {isRecording && `Duration: ${recordingDuration}s`}
            </p>
          </>
        )}
      </div>
    </div>
  );
}

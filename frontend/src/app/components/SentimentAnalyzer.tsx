'use client';

import { useState } from 'react';

// Make sure this matches your actual API URL
const API_URL = 'https://imdb-sentiment-api-b4k.onrender.com';

export default function SentimentAnalyzer() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<{
    sentiment: string;
    confidence: number;
    text: string;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeSentiment = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // First check if the API is accessible
      const healthCheck = await fetch(`${API_URL}/`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      if (!healthCheck.ok) {
        throw new Error('API is not accessible');
      }
      
      // Make the sentiment analysis request
      const response = await fetch(
        `${API_URL}/predict?text=${encodeURIComponent(text)}`,
        {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          }
        }
      );
      
      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(
          `API Error: ${response.status} - ${errorData || response.statusText}`
        );
      }
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
          setError(
            'Unable to connect to the API. Please check your internet connection and try again.'
          );
        } else if (error.message.includes('API is not accessible')) {
          setError(
            'The API service is currently unavailable. Please try again later.'
          );
        } else {
          setError(
            `Failed to analyze sentiment: ${error.message}`
          );
        }
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your movie review here..."
        className="w-full h-32 p-4 rounded-lg bg-gray-800 border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition duration-200"
      />

      <button
        onClick={analyzeSentiment}
        disabled={loading || !text.trim()}
        className={`w-full py-3 rounded-lg font-semibold transition duration-200 ${
          loading || !text.trim()
            ? 'bg-gray-700 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Analyzing...' : 'Analyze Sentiment'}
      </button>

      {error && (
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 p-6 rounded-lg bg-gray-800 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Analysis Result</h2>
            <span
              className={`px-4 py-1 rounded-full text-sm font-medium ${
                result.sentiment === 'positive'
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'
              }`}
            >
              {result.sentiment.toUpperCase()}
            </span>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Confidence</span>
              <span className="font-medium">
                {(result.confidence * 100).toFixed(1)}%
              </span>
            </div>
            
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${
                  result.sentiment === 'positive'
                    ? 'bg-green-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${result.confidence * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 
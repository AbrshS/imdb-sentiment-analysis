import SentimentAnalyzer from './components/SentimentAnalyzer';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white p-4">
      <div className="max-w-3xl mx-auto pt-20 px-4">
        <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text">
          IMDB Sentiment Analysis
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Enter your movie review to analyze its sentiment
        </p>

        <SentimentAnalyzer />
      </div>
    </main>
  );
}

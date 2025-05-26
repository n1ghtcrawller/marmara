// app/page.js
import Link from 'next/link';

export default function Home() {
  return (
      <main className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white flex items-center justify-center px-4">
        <div className="max-w-3xl text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Marmara Project
          </h1>
          <p className="text-lg md:text-xl text-gray-300 mb-8">
            Погрузитесь в мир современной <span className="text-teal-400 font-semibold">речевой аналитики</span>.
            Распознавайте, анализируйте и получайте инсайты из аудио в пару кликов.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
                href="/login"
                className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-xl font-medium shadow-lg transition text-center"
            >
              Войти
            </Link>
            <Link
                href="/register"
                className="bg-white hover:bg-gray-100 text-teal-700 px-6 py-3 rounded-xl font-medium shadow-lg transition text-center"
            >
              Попробовать сейчас
            </Link>
          </div>
          <div className="mt-12 text-sm text-gray-500">
            Используется <span className="text-gray-300">Whisper</span>, <span className="text-gray-300">spaCy</span>, <span className="text-gray-300">nltk</span> и другие библиотеки для точного анализа речи.
          </div>
        </div>
      </main>
  );
}

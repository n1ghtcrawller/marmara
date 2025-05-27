'use client';

import { useEffect, useState } from 'react';

export default function HistoryPage() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await fetch('http://localhost:8000/results', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (!res.ok) {
                    throw new Error('Ошибка при получении данных');
                }

                const data = await res.json();
                setResults(data);
            } catch (err) {
                setError('Не удалось загрузить результаты');
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, []);

    return (
        <main className="min-h-screen px-4 py-10 bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold mb-8 text-center">История загрузок и анализов</h1>

                {loading && <p className="text-center text-gray-400">Загрузка...</p>}
                {error && <p className="text-center text-red-500">{error}</p>}

                {results.length === 0 && !loading && (
                    <p className="text-center text-gray-500">Пока нет загруженных файлов</p>
                )}

                <div className="space-y-6">
                    {results.map((item) => (
                        <div
                            key={item.id}
                            className="bg-gray-800 rounded-xl shadow-md p-6 border border-gray-700 hover:shadow-lg transition"
                        >
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-teal-400 font-semibold"># {item.id}</span>
                                <span className="text-sm text-gray-400">
                {new Date(item.created_at).toLocaleString('ru-RU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                })}
            </span>
                            </div>
                            {item.text === null ? (
                                <p className="text-yellow-400 italic animate-pulse">Обработка...</p>
                            ) : (
                                <p className="text-gray-100 whitespace-pre-wrap">{item.text}</p>
                            )}
                        </div>
                    ))}

                </div>
            </div>
        </main>
    );
}

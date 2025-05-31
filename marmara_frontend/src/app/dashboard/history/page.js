'use client';

import { useEffect, useState } from 'react';
import { TrashIcon, ClipboardIcon } from '@heroicons/react/24/outline';

export default function HistoryPage() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

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

    useEffect(() => {
        fetchResults();
    }, []);

    const handleDelete = async (id) => {
        const confirmed = window.confirm(`Удалить результат #${id}?`);
        if (!confirmed) return;

        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`http://localhost:8000/results/${id}`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!res.ok) {
                throw new Error('Ошибка при удалении');
            }

            setResults(results.filter((r) => r.id !== id));
        } catch (err) {
            alert('Ошибка при удалении записи');
        }
    };

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
                            className="bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-700 hover:border-teal-500 transition-all group"
                        >
                            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                                <div className="flex-1">
                                    <span className="text-teal-400 font-semibold text-sm"># {item.id}</span>
                                    <div className="text-sm text-gray-400">
                                        {new Date(item.created_at).toLocaleString('ru-RU', {
                                            day: '2-digit',
                                            month: '2-digit',
                                            year: 'numeric',
                                            hour: '2-digit',
                                            minute: '2-digit',
                                        })}
                                    </div>
                                </div>

                                <div className="flex gap-2 items-center">
                                    {item.text && (
                                        <button
                                            onClick={() => {
                                                navigator.clipboard.writeText(item.text);
                                                alert('Текст скопирован в буфер обмена!');
                                            }}
                                            title="Скопировать текст"
                                            className="p-2 bg-blue-600 hover:bg-blue-700 rounded-full text-white shadow-md transition"
                                        >
                                            <ClipboardIcon className="h-5 w-5" />
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleDelete(item.id)}
                                        title="Удалить"
                                        className="p-2 bg-red-600 hover:bg-red-700 rounded-full text-white shadow-md transition"
                                    >
                                        <TrashIcon className="h-5 w-5" />
                                    </button>
                                </div>
                            </div>

                            {item.audio_url && item.audio_url._url && (
                                <audio
                                    controls
                                    className="w-full mt-4 rounded-lg bg-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-400"
                                >
                                    <source src={item.audio_url._url} type="audio/ogg" />
                                    Ваш браузер не поддерживает аудио.
                                </audio>
                            )}

                            {item.text === null ? (
                                <p className="text-yellow-400 italic animate-pulse mt-4">⏳ Обработка...</p>
                            ) : (
                                <p className="text-gray-100 whitespace-pre-wrap mt-4">{item.text}</p>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </main>
    );
}

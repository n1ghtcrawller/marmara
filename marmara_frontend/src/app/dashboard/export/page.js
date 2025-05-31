'use client';

import { useEffect, useState } from 'react';

export default function ExportPage() {
    const [transcriptions, setTranscriptions] = useState([]);
    const [reports, setReports] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    useEffect(() => {
        const fetchData = async () => {
            if (!token) {
                setError('Не найден токен авторизации');
                setLoading(false);
                return;
            }

            try {
                const transRes = await fetch('http://localhost:8000/results', {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!transRes.ok) throw new Error('Ошибка при получении транскрипций');
                const transData = await transRes.json();
                setTranscriptions(transData);

                const reportRes = await fetch('http://localhost:8000/reports/', {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!reportRes.ok) throw new Error('Ошибка при получении отчетов');
                const reportData = await reportRes.json();

                const reportMap = {};
                reportData.forEach((report) => {
                    reportMap[report.transcription_id] = report;
                });

                setReports(reportMap);
            } catch (err) {
                setError(err.message || 'Произошла ошибка');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [token]);

    const handleCreateReport = async (transcriptionId) => {
        if (!token) return;

        try {
            const res = await fetch(`http://localhost:8000/reports/${transcriptionId}`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (!res.ok) throw new Error('Ошибка при создании отчета');
            const newReport = await res.json();

            setReports((prev) => ({
                ...prev,
                [transcriptionId]: newReport
            }));
        } catch (err) {
            alert(err.message || 'Ошибка при создании отчета');
        }
    };

    const handleExport = (format, reportId) => {
        alert(`Экспорт в ${format} для отчёта #${reportId} (заглушка)`);
    };

    return (
        <div className="p-6">
            <h1 className="text-3xl font-semibold mb-4">Экспорт данных</h1>
            <p className="mb-6 text-gray-600">Экспорт транскриптов и отчетов в разные форматы.</p>

            {loading && <p>Загрузка...</p>}
            {error && <p className="text-red-500">{error}</p>}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {transcriptions.map((t) => {
                    const report = reports[t.id];

                    return (
                        <div
                            key={t.id}
                            className="bg-white rounded-2xl shadow p-5 border border-gray-100"
                        >
                            <h2 className="text-xl font-semibold mb-2">Транскрипция #{t.id}</h2>
                            <p className="text-sm text-gray-500 mb-2">
                                Дата: {new Date(t.created_at).toLocaleString()}
                            </p>

                            {report ? (
                                <>
                                    <ul className="text-gray-700 mb-4 text-sm space-y-1">
                                        <li>👋 Приветствие: {report.greeting ? 'Да' : 'Нет'}</li>
                                        <li>🎁 Скидка предложена: {report.offered_discount ? 'Да' : 'Нет'}</li>
                                        <li>📦 Спецтариф: {report.offered_special_tariff ? 'Да' : 'Нет'}</li>
                                        <li>🤝 Дружелюбность: {report.friendliness_score ?? 'N/A'}/10</li>
                                        <li>📌 Продукт: {report.product_interest || '—'}</li>
                                        <li>🧠 Источник клиента: {report.client_knows_source ? 'Да' : 'Нет'}</li>
                                    </ul>

                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => handleExport('JSON', report.id)}
                                            className="bg-blue-500 hover:bg-blue-600 text-white text-sm px-4 py-2 rounded-lg"
                                        >
                                            Экспорт в JSON
                                        </button>
                                        <button
                                            onClick={() => handleExport('PDF', report.id)}
                                            className="bg-purple-500 hover:bg-purple-600 text-white text-sm px-4 py-2 rounded-lg"
                                        >
                                            Экспорт в PDF
                                        </button>
                                    </div>
                                </>
                            ) : (
                                <button
                                    onClick={() => handleCreateReport(t.id)}
                                    className="bg-green-500 hover:bg-green-600 text-white text-sm px-4 py-2 rounded-lg mt-4"
                                >
                                    Создать отчёт
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

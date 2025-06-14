'use client';

import { useEffect, useState } from 'react';

export default function ExportPage() {
    const [transcriptions, setTranscriptions] = useState([]);
    const [reports, setReports] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);


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

                const generatingIds = reportData
                    .filter((r) => r.llm_analysis === "generating")
                    .map((r) => r.transcription_id);

                if (generatingIds.length > 0) {
                    setTimeout(fetchData, 3000);
                }
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
        setIsLoading(true);
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
        } finally {
            setIsLoading(false);
        }
    };

    const handleExport = (format, reportId) => {
        alert(`Экспорт в ${format} для отчёта #${reportId} (заглушка)`);
    };
    const handleAnalyzeLLM = async (reportId, transcriptionId) => {
        if (!token || !reportId) {
            console.warn('Пустой reportId, анализ невозможен');
            return;
        }
        setIsLoading(true);
        try {
            const res = await fetch(`http://localhost:8000/reports/report/${reportId}/analyze-llm`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (!res.ok) throw new Error('Ошибка при анализе отчета LLM');
            const updatedReport = await res.json();

            setReports((prev) => ({
                ...prev,
                [transcriptionId]: updatedReport
            }));
        } catch (err) {
            alert(err.message || 'Ошибка при анализе LLM');
        } finally {
            setIsLoading(false);
        }
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
                    const isProcessing = !t.text;

                    return (
                        <div
                            key={t.id}
                            className="bg-white rounded-2xl shadow p-5 border border-gray-100"
                        >
                            <h2 className="text-xl text-black font-semibold mb-2">Транскрипция #{t.id}</h2>
                            <p className="text-sm text-gray-500 mb-2">
                                Дата: {new Date(t.created_at).toLocaleString()}
                            </p>

                            {isProcessing ? (
                                <p className="text-gray-500 italic">Запись ещё обрабатывается...</p>
                            ) : report ? (
                                <>
                                    <ul className="text-gray-700 mb-4 text-sm space-y-1">
                                        <li>👋 Приветствие: {report.greeting ? 'Да' : 'Нет'}</li>
                                        <li>🎁 Скидка предложена: {report.offered_discount ? 'Да' : 'Нет'}</li>
                                        <li>📦 Спецтариф: {report.offered_special_tariff ? 'Да' : 'Нет'}</li>
                                        <li>🤝 Клиентоориентированность: {report.friendliness_score ?? 'N/A'}/10</li>
                                        <li>📌 Продукт: {report.product_interest || '—'}</li>
                                        <li>🧠 Источник клиента: {report.client_knows_source ? 'Да' : 'Нет'}</li>
                                        <li className="flex items-center gap-2">
                                            Анализ от ChatGPT:
                                            {report.llm_analysis === "generating" ? (
                                                <span className="flex items-center text-yellow-600 italic">
                                                  <svg
                                                      className="animate-spin h-4 w-4 mr-1 text-yellow-500"
                                                      xmlns="http://www.w3.org/2000/svg"
                                                      fill="none"
                                                      viewBox="0 0 24 24"
                                                  >
                                                    <circle
                                                        className="opacity-25"
                                                        cx="12"
                                                        cy="12"
                                                        r="10"
                                                        stroke="currentColor"
                                                        strokeWidth="4"
                                                    />
                                                    <path
                                                        className="opacity-75"
                                                        fill="currentColor"
                                                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                                                    />
                                                  </svg>
                                                  Генерация...
                                                </span>
                                            ) : (
                                                <span>{report.llm_analysis || "—"}</span>
                                            )}
                                        </li>


                                    </ul>

                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => handleAnalyzeLLM(report.id, t.id)}
                                            className="bg-yellow-500 hover:bg-yellow-600 text-white text-sm px-4 py-2 rounded-lg"
                                        >
                                            Анализ ChatGPT
                                        </button>
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
                            ) : isLoading ? (
                                <div className="mt-4 flex items-center justify-center text-sm text-gray-500 gap-2">
                                    <svg className="animate-spin h-5 w-5 text-green-500" viewBox="0 0 24 24">
                                        <circle
                                            className="opacity-25"
                                            cx="12"
                                            cy="12"
                                            r="10"
                                            stroke="currentColor"
                                            strokeWidth="4"
                                            fill="none"
                                        />
                                        <path
                                            className="opacity-75"
                                            fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                                        />
                                    </svg>
                                    Создание отчёта...
                                </div>
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

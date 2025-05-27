'use client';

import { useEffect, useState } from 'react';
import {
    LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

const COLORS = ['#00C49F', '#FF8042', '#FFBB28', '#0088FE'];

export default function AnalyticsPage() {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await fetch('http://localhost:8000/metrics', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                const data = await res.json();
                setMetrics(data);
            } catch (e) {
                console.error('Ошибка при загрузке метрик:', e);
            } finally {
                setLoading(false);
            }
        };
        fetchMetrics();
    }, []);

    if (loading) {
        return <p className="text-center text-gray-300 mt-10">Загрузка метрик...</p>;
    }

    if (!metrics) {
        return <p className="text-center text-red-500 mt-10">Ошибка загрузки метрик</p>;
    }

    return (
        <main className="min-h-screen px-4 py-10 bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white">
            <div className="max-w-6xl mx-auto">
                <h1 className="text-3xl font-bold mb-8 text-center">Аналитика аудио и анализов</h1>

                <div className="grid md:grid-cols-2 gap-10">
                    {/* Кол-во загруженных файлов по дням */}
                    <div className="bg-gray-800 p-6 rounded-xl shadow">
                        <h2 className="text-xl font-semibold mb-4">Загрузки по дням</h2>
                        <ResponsiveContainer width="100%" height={250}>
                            <LineChart data={metrics.uploads_per_day}>
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="count" stroke="#00C49F" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Распределение по языкам */}
                    <div className="bg-gray-800 p-6 rounded-xl shadow">
                        <h2 className="text-xl font-semibold mb-4">Языки распознанной речи</h2>
                        <ResponsiveContainer width="100%" height={250}>
                            <PieChart>
                                <Pie
                                    data={metrics.languages}
                                    dataKey="value"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={80}
                                    fill="#8884d8"
                                    label
                                >
                                    {metrics.languages.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Распределение по длине аудио */}
                    <div className="bg-gray-800 p-6 rounded-xl shadow">
                        <h2 className="text-xl font-semibold mb-4">Длина аудио (по категориям)</h2>
                        <ResponsiveContainer width="100%" height={250}>
                            <BarChart data={metrics.length_distribution}>
                                <XAxis dataKey="range" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#FF8042" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Распределение по категориям анализа */}
                    <div className="bg-gray-800 p-6 rounded-xl shadow">
                        <h2 className="text-xl font-semibold mb-4">Категории анализа</h2>
                        <ResponsiveContainer width="100%" height={250}>
                            <BarChart data={metrics.analysis_types}>
                                <XAxis dataKey="type" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#FFBB28" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </main>
    );
}

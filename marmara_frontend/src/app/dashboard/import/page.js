'use client';

import { useState, useCallback } from 'react';

export default function Dashboard() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Функция обработки загрузки файла
    const uploadFile = async (file) => {
        setLoading(true);
        setError('');

        try {
            const formData = new FormData();
            const token = localStorage.getItem('token');
            formData.append('file', file);

            // Здесь отправка на сервер, например /api/upload
            const res = await fetch('http://localhost:8000/upload', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                method: 'POST',
                body: formData,
            });

            if (!res.ok) {
                throw new Error('Ошибка загрузки файла');
            }

            // Получаем результат или подтверждение
            const data = await res.json();

            setFiles(prev => [...prev, { name: file.name, status: 'Обработан', id: data.id }]);
        } catch (e) {
            setError(e.message || 'Ошибка загрузки');
        } finally {
            setLoading(false);
        }
    };

    // Обработка файлов после дропа или выбора
    const handleFiles = useCallback(
        (selectedFiles) => {
            Array.from(selectedFiles).forEach(uploadFile);
        },
        []
    );

    // События Drag & Drop
    const handleDrop = (e) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFiles(e.dataTransfer.files);
            e.dataTransfer.clearData();
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white p-8 flex flex-col items-center">
            <h1 className="text-4xl font-bold mb-6">Дашборд Marmara</h1>

            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className="w-full max-w-2xl p-16 border-4 border-dashed border-teal-500 rounded-xl text-center cursor-pointer mb-6"
            >
                <p className="text-teal-400 mb-2">Перетащите аудио-файлы сюда или выберите вручную</p>
                <input
                    type="file"
                    accept="audio/*"
                    multiple
                    className="hidden"
                    id="fileInput"
                    onChange={(e) => handleFiles(e.target.files)}
                />
                <label
                    htmlFor="fileInput"
                    className="inline-block mt-2 px-6 py-3 bg-teal-600 hover:bg-teal-700 rounded cursor-pointer"
                >
                    Выбрать файлы
                </label>
            </div>

            {loading && <p className="text-yellow-400 mb-4">Загрузка и обработка...</p>}
            {error && <p className="text-red-500 mb-4">{error}</p>}

            <ul className="w-full max-w-2xl">
                {files.map((file, idx) => (
                    <li key={idx} className="py-2 border-b border-gray-700 flex justify-between">
                        <span>{file.name}</span>
                        <span className="text-teal-400">{file.status}</span>
                    </li>
                ))}
            </ul>
        </main>
    );
}

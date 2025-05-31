'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function SearchPage() {
    const [results, setResults] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [categories, setCategories] = useState({
        маты: ['хуй', 'бля', 'пизд'],
        паразиты: ['ну', 'короче', 'вот', 'типа'],
    });
    const [selectedCategory, setSelectedCategory] = useState('');
    const [customCategoryName, setCustomCategoryName] = useState('');
    const [customWords, setCustomWords] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            setError('Токен не найден. Пожалуйста, авторизуйтесь.');
            return;
        }

        axios
            .get('http://localhost:8000/results', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => setResults(response.data))
            .catch((err) => {
                console.error(err);
                setError('Ошибка загрузки данных. Проверьте токен или сервер.');
            });
    }, []);

    const highlight = (text, words) => {
        if (!words || words.length === 0) return text;
        const pattern = new RegExp(`\\b(${words.join('|')})\\b`, 'gi');
        return text.split(pattern).map((part, i) =>
            words.includes(part.toLowerCase()) ? (
                <mark key={i} className="bg-yellow-300">{part}</mark>
            ) : part
        );
    };

    const handleAddCategory = () => {
        if (customCategoryName && customWords) {
            const wordList = customWords.split(',').map(w => w.trim().toLowerCase());
            setCategories(prev => ({ ...prev, [customCategoryName]: wordList }));
            setCustomCategoryName('');
            setCustomWords('');
        }
    };

    const filteredResults = results.filter(res =>
        searchQuery === '' ||
        res.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (selectedCategory && categories[selectedCategory]?.some(word =>
            res.text.toLowerCase().includes(word)
        ))
    );

    return (
        <div className="p-4">
            <h1 className="text-3xl font-semibold mb-4">Поиск по тексту</h1>

            <div className="flex gap-4 mb-4">
                <input
                    type="text"
                    placeholder="Введите слово для поиска"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    className="border p-2 w-1/3 rounded"
                />

                <select
                    value={selectedCategory}
                    onChange={e => setSelectedCategory(e.target.value)}
                    className="border p-2 rounded"
                >
                    <option value="">Выберите категорию</option>
                    {Object.keys(categories).map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                    ))}
                </select>
            </div>

            <div className="mb-6">
                <h2 className="font-bold">Добавить свою категорию</h2>
                <div className="flex gap-2 mt-2">
                    <input
                        type="text"
                        placeholder="Название категории (например: медицинские)"
                        value={customCategoryName}
                        onChange={e => setCustomCategoryName(e.target.value)}
                        className="border p-2 w-1/3 rounded"
                    />
                    <input
                        type="text"
                        placeholder="Слова через запятую (например: метформин,аспирин)"
                        value={customWords}
                        onChange={e => setCustomWords(e.target.value)}
                        className="border p-2 w-1/2 rounded"
                    />
                    <button
                        onClick={handleAddCategory}
                        className="bg-blue-600 text-white px-4 py-2 rounded"
                    >
                        Добавить
                    </button>
                </div>
            </div>

            <div className="space-y-6">
                {filteredResults.map((res) => (
                    <div key={res.id} className="p-4 border rounded shadow">
                        <p className="text-gray-600 text-sm">{new Date(res.created_at).toLocaleString()}</p>
                        <audio controls src={res.audio_url._url} className="my-2" />
                        <p className="text-lg">
                            {highlight(res.text, [
                                ...(
                                    selectedCategory ? categories[selectedCategory] : []
                                ),
                                ...(searchQuery ? [searchQuery.toLowerCase()] : []),
                            ])}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}

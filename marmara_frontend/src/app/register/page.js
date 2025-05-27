'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleRegister = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch('http://localhost:8000/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (res.ok) {
                setSuccess(true);
                setTimeout(() => router.push('/login'), 1500);
            } else {
                const data = await res.json();
                setError(data.detail || 'Ошибка при регистрации');
            }
        } catch (err) {
            setError('Ошибка подключения к серверу');
        }
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 flex items-center justify-center px-4 text-white">
            <form
                onSubmit={handleRegister}
                className="bg-gray-900 p-8 rounded-xl shadow-lg w-full max-w-sm"
            >
                <h1 className="text-2xl font-bold mb-6 text-center">Регистрация в Marmara</h1>

                {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
                {success && <p className="text-green-500 text-sm mb-4">Успешно! Перенаправляем...</p>}

                <input
                    type="text"
                    placeholder="Имя пользователя"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full mb-4 p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    required
                />
                <input
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full mb-6 p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    required
                />
                <button
                    type="submit"
                    className="w-full bg-teal-600 hover:bg-teal-700 transition text-white py-2 rounded"
                >
                    Зарегистрироваться
                </button>

                <p className="text-sm text-gray-400 mt-4 text-center">
                    Уже есть аккаунт?{' '}
                    <a href="/login" className="text-teal-400 hover:underline">
                        Войти
                    </a>
                </p>
            </form>
        </main>
    );
}

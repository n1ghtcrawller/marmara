'use client';

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const router = useRouter()

    const handleSubmit = async (e) => {
        e.preventDefault()

        const body = new URLSearchParams()
        body.append('username', username)
        body.append('password', password)

        try {
            const res = await fetch('http://localhost:8000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: body.toString(),
            })

            if (res.ok) {
                const data = await res.json()
                localStorage.setItem('token', data.access_token)
                router.push('/dashboard')
            } else {
                const data = await res.json()
                setError(data.detail || 'Ошибка авторизации')
            }
        } catch {
            setError('Ошибка подключения к серверу')
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen px-4">
            <form className="bg-gray-900 p-8 rounded-2xl shadow-xl w-full max-w-sm" onSubmit={handleSubmit}>
                <h2 className="text-2xl font-bold mb-6 text-center">Вход в Marmara</h2>

                {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}

                <input
                    type="text"
                    placeholder="Имя пользователя"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full p-3 mb-4 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    required
                />
                <input
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full p-3 mb-6 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    required
                />
                <button
                    type="submit"
                    className="w-full bg-teal-600 hover:bg-teal-700 text-white py-2 rounded-lg transition"
                >
                    Войти
                </button>
            </form>
        </div>
    )
}

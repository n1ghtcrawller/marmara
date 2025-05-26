'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const router = useRouter()

    const handleSubmit = async (e) => {
        e.preventDefault()
        console.log('Logging in', email)
        router.push('/dashboard')
    }

    return (
        <div className="flex items-center justify-center min-h-screen px-4">
            <form className="bg-gray-900 p-8 rounded-2xl shadow-xl w-full max-w-sm" onSubmit={handleSubmit}>
                <h2 className="text-2xl font-bold mb-6 text-center">Вход в Marmara</h2>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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

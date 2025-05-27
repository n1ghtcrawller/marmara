'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

const menuItems = [
    { id: 'history', label: 'История загрузок и анализов', href: '/dashboard/history' },
    { id: 'visualization', label: 'Визуализация данных', href: '/dashboard/visualization' },
    { id: 'tags', label: 'Теги и категории', href: '/dashboard/tags' },
    { id: 'upload', label: 'Импорт записей', href: '/dashboard/import' },
    { id: 'notifications', label: 'Уведомления и алерты', href: '/dashboard/notifications' },
    { id: 'export', label: 'Экспорт данных', href: '/dashboard/export' },
    { id: 'settings', label: 'Пользовательские настройки', href: '/dashboard/settings' },
    { id: 'accounts', label: 'Мультиаккаунты и роли', href: '/dashboard/accounts' },
    { id: 'search', label: 'Поиск по тексту', href: '/dashboard/search' },
    { id: 'integration', label: 'Интеграция с внешними сервисами', href: '/dashboard/integration' },
    { id: 'tasks', label: 'Автоматическое создание задач', href: '/dashboard/tasks' },
];

export default function DashboardLayout({ children }) {
    const pathname = usePathname();
    const router = useRouter();

    const handleLogout = () => {
        // Здесь можно добавить логику выхода, очистки сессии, токенов и т.д.
        // Например, вызвать API logout, очистить cookies, localStorage и т.п.
        // После выхода — редирект на страницу логина:
        router.push('/login');
    };

    return (
        <main className="flex min-h-screen bg-gradient-to-tr from-indigo-900 via-black to-indigo-800 text-white font-sans">
            {/* Sidebar */}
            <nav className="w-64 bg-gray-900 border-r border-indigo-700 p-6 flex flex-col">
                <h2 className="text-2xl font-bold mb-8 text-indigo-400">Меню</h2>
                <ul className="space-y-4 flex-grow">
                    {menuItems.map(({ id, label, href }) => {
                        const isActive = pathname === href;
                        return (
                            <li key={id}>
                                <Link
                                    href={href}
                                    className={`block w-full text-left px-4 py-2 rounded-lg transition
                    ${
                                        isActive
                                            ? 'bg-indigo-600 text-white font-semibold shadow-lg'
                                            : 'hover:bg-indigo-700 text-indigo-300'
                                    }`}
                                >
                                    {label}
                                </Link>
                            </li>
                        );
                    })}
                </ul>

                {/* Кнопка выхода */}
                <button
                    onClick={handleLogout}
                    className="mt-6 bg-red-600 hover:bg-red-700 transition-colors py-2 px-4 rounded-lg font-semibold shadow-lg"
                >
                    Выйти
                </button>

                <div className="mt-auto text-indigo-400 text-sm opacity-70 select-none">
                    © 2025 Audio Analytics
                </div>
            </nav>

            {/* Main content */}
            <section className="flex-1 p-8 overflow-auto">{children}</section>
        </main>
    );
}

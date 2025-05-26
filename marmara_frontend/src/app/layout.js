import './globals.css'

export const metadata = {
    title: 'Marmara Project',
    description: 'Современная речевая аналитика',
}

export default function RootLayout({ children }) {
    return (
        <html lang="ru">
        <body className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white">
        {children}
        </body>
        </html>
    )
}

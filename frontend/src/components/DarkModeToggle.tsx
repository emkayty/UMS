'use client'

import { useTheme } from '@/lib/theme'

export function DarkModeToggle() {
  const { theme, setTheme, isDark } = useTheme()

  const toggleTheme = () => {
    if (theme === 'light') setTheme('dark')
    else if (theme === 'dark') setTheme('system')
    else setTheme('light')
  }

  const icons = {
    light: '☀️',
    dark: '🌙',
    system: '💻',
  }

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      aria-label={`Current theme: ${theme}. Click to change.`}
      title={`Theme: ${theme}`}
    >
      <span className="text-xl" role="img" aria-hidden="true">
        {icons[theme]}
      </span>
    </button>
  )
}

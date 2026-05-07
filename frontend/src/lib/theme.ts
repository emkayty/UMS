/**
 * UMS Frontend - Theme Module
 * Theme management for dark/light mode
 */

'use client';

import { useState, useEffect } from 'react';

// Theme type
type Theme = 'light' | 'dark' | 'system';

// Get stored theme or use system preference
function getStoredTheme(): Theme {
  if (typeof window === 'undefined') return 'light';
  const stored = localStorage.getItem('ums_theme') as Theme;
  if (stored) return stored;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Theme context hook
export function useTheme() {
  const [theme, setThemeState] = useState<Theme>('light');
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const stored = getStoredTheme();
    setThemeState(stored);
    setIsDark(stored === 'dark');
    document.documentElement.classList.toggle('dark', stored === 'dark');
  }, []);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    setIsDark(newTheme === 'dark');
    if (typeof window !== 'undefined') {
      localStorage.setItem('ums_theme', newTheme);
    }
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return { theme, setTheme, toggleTheme, isDark };
}

// Export for component use
export default useTheme;
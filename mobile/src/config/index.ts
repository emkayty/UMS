/**
 * UMS Mobile - Configuration
 * Mobile app configuration
 */

const CONFIG = {
  // API Configuration
  API_BASE_URL: 'http://localhost:8000',
  API_PREFIX: '/api/v1',
  
  // App Configuration
  NAME: 'UniCore',
  VERSION: '2.0.0',
  
  // Auth
  AUTH_TOKEN_KEY: 'ums_auth_token',
  
  // Pagination
  PAGE_SIZE: 20,
  
  // Timeouts
  REQUEST_TIMEOUT: 30000,
  
  // Feature Flags
  FEATURES: {
    ENABLE_QR_ATTENDANCE: true,
    ENABLE_ONLINE_PAYMENT: true,
    ENABLE_LIBRARY: true,
    ENABLE_HOSTEL: true,
    ENABLE_AI: true,
  },
};

// Theme Colors (Nigerian-inspired + Modern)
const COLORS = {
  // Primary
  primary: '#1e40af',      // Deep blue
  primaryLight: '#3b82f6',
  primaryDark: '#1e3a8a',
  
  // Secondary  
  secondary: '#7c3aed',   // Purple
  secondaryLight: '#a78bfa',
  
  // Accent (Green - Nigeria flag inspired)
  accent: '#10b981',
  accentLight: '#34d399',
  
  // Neutral
  white: '#ffffff',
  black: '#000000',
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  
  // Status
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Border
  border: '#e5e7eb',
};

export { CONFIG, COLORS };
export default CONFIG;
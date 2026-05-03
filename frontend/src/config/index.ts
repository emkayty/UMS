/**
 * Frontend Configuration
 */

export const APP_CONFIG = {
  appName: 'UMS',
  appVersion: '1.0.0',
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  
  auth: {
    tokenKey: 'ums_auth_token',
    refreshKey: 'ums_refresh_token',
    tokenExpiry: 3600,
  },
  
  api: {
    timeout: 30000,
    retries: 3,
  },
  
  pagination: {
    defaultPageSize: 20,
    maxPageSize: 100,
  },
};

export const API_ENDPOINTS = {
  auth: {
    login: '/api/v1/auth/login',
    register: '/api/v1/auth/register',
    logout: '/api/v1/auth/logout',
    refresh: '/api/v1/auth/refresh',
    me: '/api/v1/auth/me',
  },
  
  students: {
    list: '/api/v1/students',
    detail: (id: string) => `/api/v1/students/${id}`,
    create: '/api/v1/students',
    update: (id: string) => `/api/v1/students/${id}`,
    delete: (id: string) => `/api/v1/students/${id}`,
  },
  
  staff: {
    list: '/api/v1/staff',
    detail: (id: string) => `/api/v1/staff/${id}`,
  },
  
  courses: {
    list: '/api/v1/courses',
    enroll: '/api/v1/courses/enroll',
  },
  
  fees: {
    list: '/api/v1/fees',
    payments: '/api/v1/fees/payments',
  },
  
  reports: {
    analytics: '/api/v1/reports/analytics',
    export: '/api/v1/reports/export',
  },
};

export const ROUTES = {
  home: '/',
  login: '/login',
  dashboard: '/dashboard',
  students: '/dashboard/students',
  courses: '/dashboard/courses',
  fees: '/dashboard/fees',
  reports: '/dashboard/reports',
  settings: '/dashboard/settings',
};


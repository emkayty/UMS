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
  // Authentication
  auth: {
    login: '/api/v1/auth/login',
    register: '/api/v1/auth/register',
    logout: '/api/v1/auth/logout',
    refresh: '/api/v1/auth/refresh',
    me: '/api/v1/auth/me',
  },
  
  // Students
  students: {
    list: '/api/v1/students',
    detail: (id: string) => `/api/v1/students/${id}`,
    create: '/api/v1/students',
    update: (id: string) => `/api/v1/students/${id}`,
    delete: (id: string) => `/api/v1/students/${id}`,
  },
  
  // Staff
  staff: {
    list: '/api/v1/staff',
    detail: (id: string) => `/api/v1/staff/${id}`,
  },
  
  // Courses
  courses: {
    list: '/api/v1/courses',
    enroll: '/api/v1/courses/enroll',
  },
  
  // Fees & Payments
  fees: {
    list: '/api/v1/fees',
    payments: '/api/v1/fees/payments',
    invoice: '/api/v1/fees/invoice',
    initiatePayment: '/api/v1/payments/initiate',
    verifyPayment: '/api/v1/payments/verify',
  },
  
  // Reports
  reports: {
    analytics: '/api/v1/reports/analytics',
    export: '/api/v1/reports/export',
  },
  
  // ADMISSION MODULE
  admissions: {
    list: '/api/v1/applications',
    detail: (id: string) => `/api/v1/applications/${id}`,
    submit: '/api/v1/applications/submit',
    statusCheck: '/api/v1/applications/status',
  },
  
  // TRANSCRIPT MODULE
  transcripts: {
    list: '/api/v1/transcripts',
    request: '/api/v1/transcripts/request',
    detail: (id: string) => `/api/v1/transcripts/${id}`,
  },
  
  // HOSTEL MODULE
  hostels: {
    list: '/api/v1/hostels',
    available: '/api/v1/hostels/available',
    detail: (id: string) => `/api/v1/hostels/${id}`,
    apply: '/api/v1/hostel-applications/apply',
  },
  
  // CLEARANCE MODULE
  clearance: {
    list: '/api/v1/clearance',
    apply: '/api/v1/clearance/apply',
    detail: (id: string) => `/api/v1/clearance/${id}`,
    items: '/api/v1/clearance/items',
  },
  
  // SIWES MODULE
  siwes: {
    companies: '/api/v1/siwes/companies',
    placements: '/api/v1/siwes/placements',
    logbook: '/api/v1/siwes/logbook',
    assessment: '/api/v1/siwes/assessment',
  },
  
  // ALUMNI MODULE
  alumni: {
    profile: '/api/v1/alumni/profile',
    events: '/api/v1/alumni/events',
    register: '/api/v1/alumni/register',
    jobs: '/api/v1/alumni/jobs',
  },
  
  // LIBRARY MODULE
  library: {
    books: '/api/v1/library/books',
    borrow: '/api/v1/library/borrow',
    return: '/api/v1/library/return',
    reserve: '/api/v1/library/reserve',
  },
  
  // CALENDAR MODULE
  calendar: {
    events: '/api/v1/calendar/events',
    timetable: '/api/v1/calendar/timetable',
  },
  
  // LEAVE MODULE
  leave: {
    list: '/api/v1/leave',
    apply: '/api/v1/leave/apply',
    balance: '/api/v1/leave/balance',
  },
  
  // ID CARDS MODULE
  idCards: {
    request: '/api/v1/id-cards/request',
    detail: (id: string) => `/api/v1/id-cards/${id}`,
  },
  
  // NOTIFICATIONS MODULE
  notifications: {
    list: '/api/v1/notifications',
    read: '/api/v1/notifications/read',
    preferences: '/api/v1/notifications/preferences',
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


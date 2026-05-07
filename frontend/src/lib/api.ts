/**
 * UMS Frontend - API Client
 * Unified API client for backend communication
 */

import { APP_CONFIG } from '@/config';

const API_BASE_URL = APP_CONFIG.apiUrl || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

// Helper for authenticated requests
async function authFetch(url: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('ums_token') : null;
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  return response.json();
}

// AUTH API
export const authApi = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data.token) {
        localStorage.setItem('ums_token', data.token);
      }
      return { success: true, data };
    }
    
    return { success: false, error: 'Login failed' };
  },
  
  logout: async () => {
    localStorage.removeItem('ums_token');
    return { success: true };
  },
  
  me: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/auth/me/`);
  },
  
  refresh: async (refreshToken: string) => {
    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data.token) {
        localStorage.setItem('ums_token', data.token);
      }
      return { success: true, data };
    }
    
    return { success: false };
  },
};

// STUDENT API
export const studentApi = {
  list: async (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return authFetch(`${API_BASE_URL}${API_PREFIX}/students/${query}`);
  },
  
  profile: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/students/profile/`);
  },
  
  results: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/students/results/`);
  },
  
  attendance: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/students/attendance/`);
  },
  
  courses: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/students/courses/`);
  },
};

// COURSE API
export const courseApi = {
  list: async (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return authFetch(`${API_BASE_URL}${API_PREFIX}/courses/${query}`);
  },
  
  enroll: async (courseId: string) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/courses/enroll/`, {
      method: 'POST',
      body: JSON.stringify({ course_id: courseId }),
    });
  },
};

// FINANCE API
export const financeApi = {
  invoices: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/fees/invoices/`);
  },
  
  payments: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/fees/payments/`);
  },
};

// ACADEMIC API
export const academicApi = {
  sessions: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/academic/sessions/`);
  },
  
  faculties: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/academic/faculties/`);
  },
  
  departments: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/academic/departments/`);
  },
};

// AI API
export const aiApi = {
  riskScore: async (studentId: string) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/analytics/students/${studentId}/risk-score`);
  },
  
  gradePredictions: async (studentId: string) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/analytics/students/${studentId}/grade-predictions`);
  },
  
  search: async (query: string) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/analytics/ai/search?q=${encodeURIComponent(query)}`);
  },
};

// HOSTEL API
export const hostelApi = {
  list: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/hostels/`);
  },
  
  available: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/hostels/available/`);
  },
  
  apply: async (data: any) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/hostel-applications/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

// CLEARANCE API
export const clearanceApi = {
  getStatus: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/clearance/`);
  },
  
  apply: async (data: any) => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/clearance/apply/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

// ANNOUNCEMENTS API
export const announcementApi = {
  list: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/announcements/`);
  },
};

// LIBRARY API
export const libraryApi = {
  books: async (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return authFetch(`${API_BASE_URL}${API_PREFIX}/library/books/${query}`);
  },
  
  borrow: async (bookId: string | number | { book_id: number }) => {
    // Handle both object and primitive types
    const data = typeof bookId === 'object' ? bookId : { book_id: bookId };
    return authFetch(`${API_BASE_URL}${API_PREFIX}/library/borrow/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  return: async (bookId: string | number | { book_id: number }) => {
    const data = typeof bookId === 'object' ? bookId : { book_id: bookId };
    return authFetch(`${API_BASE_URL}${API_PREFIX}/library/return/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  my: async () => {
    return authFetch(`${API_BASE_URL}${API_PREFIX}/library/my/`);
  },
};

// Default export
export default {
  auth: authApi,
  authApi: authApi,
  student: studentApi,
  studentApi: studentApi,
  course: courseApi,
  finance: financeApi,
  academic: academicApi,
  ai: aiApi,
  aiApi: aiApi,
  hostel: hostelApi,
  hostelApi: hostelApi,
  clearance: clearanceApi,
  clearanceApi: clearanceApi,
  announcement: announcementApi,
  libApi: libraryApi,
  libraryApi: libraryApi,
};
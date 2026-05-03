/**
 * SHARED API - Universal API Client
 * Used by both Frontend and Mobile
 * Serves same data from backend
 */

import { API_ENDPOINTS, APP_CONFIG } from '../config';

type Method = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface RequestConfig {
  method?: Method;
  body?: any;
  headers?: Record<string, string>;
  params?: Record<string, any>;
}

interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

/**
 * Get auth token
 */
function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(APP_CONFIG.auth.tokenKey);
  }
  return null;
}

/**
 * Set auth token
 */
function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(APP_CONFIG.auth.tokenKey, token);
  }
}

/**
 * Remove auth token
 */
function removeToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(APP_CONFIG.auth.tokenKey);
  }
}

/**
 * Make API request
 */
async function request<T = any>(
  endpoint: string,
  config: RequestConfig = {}
): Promise<ApiResponse<T> {
  const { method = 'GET', body, headers = {}, params } = config;
  
  // Build URL with params
  let url = `${APP_CONFIG.apiUrl}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams}`;
  }
  
  // Build headers
  const authToken = getToken();
  const requestHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers,
  };
  
  if (authToken) {
    requestHeaders['Authorization'] = `Bearer ${authToken}`;
  }
  
  try {
    const response = await fetch(url, {
      method,
      headers: requestHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });
    
    const data = await response.json();
    
    return {
      data,
      status: response.status,
      error: response.ok ? undefined : data.error,
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Network error',
      status: 0,
    };
  }
}

// ============================================================
// SHARED API METHODS - Match Backend exactly
// ============================================================

// Auth API
export const auth = {
  login: (email: string, password: string) =>
    request(API_ENDPOINTS.auth.login, { method: 'POST', body: { email, password } }),
  
  register: (data: any) =>
    request(API_ENDPOINTS.auth.register, { method: 'POST', body: data }),
  
  logout: () =>
    request(API_ENDPOINTS.auth.logout, { method: 'POST' }),
  
  refresh: () =>
    request(API_ENDPOINTS.auth.refresh, { method: 'POST' }),
  
  me: () =>
    request(API_ENDPOINTS.auth.me),
};

// Students API
export const students = {
  list: (params?: any) =>
    request(API_ENDPOINTS.students.list, { params }),
  
  get: (id: string) =>
    request(API_ENDPOINTS.students.detail(id)),
  
  create: (data: any) =>
    request(API_ENDPOINTS.students.create, { method: 'POST', body: data }),
  
  update: (id: string, data: any) =>
    request(API_ENDPOINTS.students.update(id), { method: 'PUT', body: data }),
  
  delete: (id: string) =>
    request(API_ENDPOINTS.students.delete(id), { method: 'DELETE' }),
};

// Courses API
export const courses = {
  list: (params?: any) =>
    request(API_ENDPOINTS.courses.list, { params }),
  
  enroll: (courseId: string) =>
    request(API_ENDPOINTS.courses.enroll, { method: 'POST', body: { courseId } }),
  
  get: (id: string) =>
    request(`/api/v1/courses/${id}`),
};

// Fees API
export const fees = {
  list: (params?: any) =>
    request(API_ENDPOINTS.fees.list, { params }),
  
  payments: () =>
    request(API_ENDPOINTS.fees.payments),
  
  pay: (feeId: string, data: any) =>
    request(`/api/v1/fees/${feeId}/pay`, { method: 'POST', body: data }),
};

// Attendance API  
export const attendance = {
  list: (params?: any) =>
    request('/api/v1/attendance', { params }),
  
  mark: (data: any) =>
    request('/api/v1/attendance/mark', { method: 'POST', body: data }),
  
  qr: (code: string) =>
    request('/api/v1/attendance/qr', { method: 'POST', body: { code } }),
};

// Results API
export const results = {
  list: (params?: any) =>
    request('/api/v1/results', { params }),
  
  get: (studentId: string) =>
    request(`/api/v1/results/${studentId}`),
  
  transcript: (studentId: string) =>
    request(`/api/v1/results/${studentId}/transcript`),
};

// Reports API
export const reports = {
  analytics: (params?: any) =>
    request(API_ENDPOINTS.reports.analytics, { params }),
  
  export: (format: string) =>
    request(API_ENDPOINTS.reports.export, { method: 'POST', body: { format } }),
};

// Staff API
export const staff = {
  list: (params?: any) =>
    request(API_ENDPOINTS.staff.list, { params }),
  
  get: (id: string) =>
    request(API_ENDPOINTS.staff.detail(id)),
};

// Institution API
export const institution = {
  get: () =>
    request('/api/v1/institution'),
  
  update: (data: any) =>
    request('/api/v1/institution', { method: 'PUT', body: data }),
};

// AI API
export const ai = {
  chat: (message: string, context?: any) =>
    request('/api/v1/ai/chat', { method: 'POST', body: { message, context } }),
  
  suggest: (query: string) =>
    request('/api/v1/ai/suggest', { method: 'POST', body: { query } }),
};

// Library API
export const library = {
  books: (params?: any) =>
    request('/api/v1/library/books', { params }),
  
  borrow: (bookId: string) =>
    request('/api/v1/library/borrow', { method: 'POST', body: { bookId } }),
  
  return: (bookId: string) =>
    request('/api/v1/library/return', { method: 'POST', body: { bookId } }),
  
  my: () =>
    request('/api/v1/library/my'),
};

// Export all
export default {
  request,
  auth,
  students,
  courses,
  fees,
  attendance,
  results,
  reports,
  staff,
  institution,
  ai,
  library,
  getToken,
  setToken,
  removeToken,
};
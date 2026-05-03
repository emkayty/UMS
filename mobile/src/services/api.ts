/**
 * UMS Mobile - API Service
 * Unified API client - matches frontend exactly
 */

import { CONFIG } from '../config';

// Use same endpoints as frontend
const API_PREFIX = CONFIG.API_PREFIX;

// ============================================================
// AUTH - Same as frontend
// ============================================================

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      const data = await response.json();
      return { success: true, data };
    }
    
    return { success: false, error: 'Login failed' };
  },
  
  logout: async () => {
    return { success: true };
  },
  
  me: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/auth/me/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// STUDENTS - Same as frontend
// ============================================================

export const studentApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/students/${query}`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  profile: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/students/profile/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  results: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/students/results/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  attendance: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/students/attendance/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  courses: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/students/courses/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// COURSES - NEW - Matches frontend
// ============================================================

export const courseApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/courses/${query}`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  enroll: async (courseId: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/courses/enroll/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ course_id: courseId }),
    });
    
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// FINANCE - Same as frontend
// ============================================================

export const financeApi = {
  invoices: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/fees/invoices/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  payments: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/fees/payments/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// ATTENDANCE - NEW - Matches frontend
// ============================================================

export const attendanceApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/attendance/${query}`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  mark: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/attendance/mark/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  qr: async (code: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/attendance/qr/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });
    
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// STAFF - NEW - Matches frontend
// ============================================================

export const staffApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/staff/${query}`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/staff/${id}/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// LIBRARY - NEW - Matches frontend
// ============================================================

export const libraryApi = {
  books: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/books/${query}`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  borrow: async (bookId: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/borrow/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ book_id: bookId }),
    });
    
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  my: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/my/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// ACADEMIC / AI
// ============================================================

export const academicApi = {
  sessions: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/academic/sessions/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

export const aiApi = {
  risk: async (studentId: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/ai/risk/?student_id=${studentId}`
    );
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  chat: async (message: string, context?: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/ai/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context }),
    });
    
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// ANNOUNCEMENTS
// ============================================================

export const announcementApi = {
  list: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/announcements/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// Export all - matches frontend exactly
export default {
  auth: authApi,
  student: studentApi,
  course: courseApi,
  finance: financeApi,
  attendance: attendanceApi,
  staff: staffApi,
  library: libraryApi,
  academic: academicApi,
  ai: aiApi,
  announcements: announcementApi,
};
/**
 * UMS Mobile - API Service
 * Central API client for mobile app
 */

import { CONFIG } from '../config';

// ============================================================
// AUTH
// ============================================================

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      const data = await response.json();
      // Save token (in secure storage in production)
      return { success: true, data };
    }
    
    return { success: false, error: 'Login failed' };
  },
  
  logout: async () => {
    // Clear token
    return { success: true };
  },
  
  me: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/auth/me/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// STUDENTS
// ============================================================

export const studentApi = {
  profile: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/students/profile/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  results: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/students/results/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  attendance: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/students/attendance/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  courses: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/students/courses/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// FINANCE
// ============================================================

export const financeApi = {
  invoices: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/fees/invoices/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  payments: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/fees/payments/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// ACADEMIC
// ============================================================

export const academicApi = {
  sessions: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/academic/sessions/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// AI
// ============================================================

export const aiApi = {
  risk: async (studentId: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/ai/risk/?student_id=${studentId}`
    );
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
  
  chatbot: async (message: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/ai/chatbot/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
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
    const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_PREFIX}/announcements/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// Export all
export default {
  auth: authApi,
  student: studentApi,
  finance: financeApi,
  academic: academicApi,
  ai: aiApi,
  announcements: announcementApi,
};
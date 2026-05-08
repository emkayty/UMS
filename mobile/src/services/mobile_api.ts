/**
 * UMS Mobile - Complete API Service
 * All backend endpoints for mobile app
 */

import { CONFIG } from '../config';

const API_PREFIX = CONFIG.API_PREFIX;
const BASE_URL = CONFIG.API_BASE_URL;

// ============================================================
// AUTH API
// ============================================================

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${BASE_URL}${API_PREFIX}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    
    if (response.ok && data.access) {
      return { success: true, data };
    }

    return { success: false, error: data.error || 'Login failed' };
  },

  logout: async () => {
    // Clear local storage
    return { success: true };
  },

  me: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/auth/me/`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  refresh: async (refreshToken: string) => {
    const response = await fetch(`${BASE_URL}${API_PREFIX}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// STUDENT API
// ============================================================

export const studentApi = {
  // Get student profile
  profile: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/students/profile/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get dashboard stats
  stats: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/students/dashboard/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get enrolled courses
  courses: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/students/courses/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get results
  results: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/students/results/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get attendance
  attendance: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/students/attendance/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get fee details
  fees: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/fees/student/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get payment history
  payments: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/fees/payments/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get announcements
  announcements: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/announcements/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// ACADEMIC API
// ============================================================

export const academicApi = {
  // Get all courses (for course registration)
  courses: async (params?: { level?: string; semester?: string }) => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const query = params ? '?' + new URLSearchParams(params as any).toString() : '';
    const response = await fetch(`${BASE_URL}${API_PREFIX}/academic/courses/${query}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get current session
  session: async () => {
    const response = await fetch(`${BASE_URL}${API_PREFIX}/academic/session/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get departments
  departments: async () => {
    const response = await fetch(`${BASE_URL}${API_PREFIX}/academic/departments/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get programmes
  programmes: async () => {
    const response = await fetch(`${BASE_URL}${API_PREFIX}/academic/programmes/`);
    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// STAFF API
// ============================================================

export const staffApi = {
  // Get staff profile
  profile: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/staff/profile/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get leave balance
  leaveBalance: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/staff/leave/balance/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get leave requests
  leaveRequests: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/staff/leave/requests/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// LEARNING API
// ============================================================

export const learningApi = {
  // Get materials
  materials: async (courseId?: string) => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const query = courseId ? `?course=${courseId}` : '';
    const response = await fetch(`${BASE_URL}${API_PREFIX}/learning/materials/${query}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get assignments
  assignments: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/learning/assignments/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get quizzes
  quizzes: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/learning/quizzes/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// HOSTEL API
// ============================================================

export const hostelApi = {
  // Get hostel applications
  applications: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/services/hostel/applications/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },

  // Get allocation
  allocation: async () => {
    const token = await getToken();
    if (!token) return { success: false };
    
    const response = await fetch(`${BASE_URL}${API_PREFIX}/services/hostel/allocation/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.ok) {
      return { success: true, data: await response.json() };
    }
    return { success: false };
  },
};

// ============================================================
// HELPERS
// ============================================================

async function getToken(): Promise<string | null> {
  try {
    const { getToken: getStoredToken } = await import('./storage');
    return await getStoredToken();
  } catch {
    return null;
  }
}

// Export all APIs
export default {
  auth: authApi,
  student: studentApi,
  academic: academicApi,
  staff: staffApi,
  learning: learningApi,
  hostel: hostelApi,
};
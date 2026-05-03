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

// ============================================================
// NEW MODULE SERVICES - Matching Frontend + Backend
// ============================================================

// ADMISSION MODULE
export const admissionApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/applications/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/applications/${id}/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  submit: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/applications/submit/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  checkStatus: async (appNumber: string, email: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/applications/status/?application_number=${appNumber}&email=${email}`
    );
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// TRANSCRIPT MODULE
export const transcriptApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/transcripts/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  request: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/transcripts/request/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/transcripts/${id}/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// HOSTEL MODULE
export const hostelApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/hostels/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  available: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/hostels/available/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/hostels/${id}/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  apply: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/hostel-applications/apply/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// CLEARANCE MODULE
export const clearanceApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/clearance/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  apply: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/clearance/apply/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/clearance/${id}/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  items: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/clearance/items/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// SIWES MODULE
export const siwesApi = {
  companies: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/siwes/companies/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  placements: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/siwes/placements/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  logbook: async (studentId: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/siwes/logbook/?student_id=${studentId}`
    );
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  assessment: async (studentId: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/siwes/assessment/?student_id=${studentId}`
    );
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// ALUMNI MODULE
export const alumniApi = {
  profile: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/alumni/profile/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  events: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/alumni/events/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  register: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/alumni/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  jobs: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/alumni/jobs/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// LIBRARY MODULE
export const libApi = {
  books: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/books/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  borrow: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/borrow/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  returnBook: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/return/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  reserve: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/library/reserve/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// CALENDAR MODULE
export const calendarApi = {
  events: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/calendar/events/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  timetable: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/calendar/timetable/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// LEAVE MODULE
export const leaveApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/leave/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  apply: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/leave/apply/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  balance: async () => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/leave/balance/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// ID CARDS MODULE
export const idCardApi = {
  request: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/id-cards/request/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  get: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/id-cards/${id}/`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// NOTIFICATIONS MODULE
export const notificationApi = {
  list: async (params?: any) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/notifications/${query}`);
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  markRead: async (id: string) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/notifications/read/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  preferences: async (data?: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/notifications/preferences/`, {
      method: data ? 'POST' : 'GET',
      headers: { 'Content-Type': 'application/json' },
      body: data ? JSON.stringify(data) : undefined,
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// PAYMENTS MODULE
export const paymentApi = {
  initiate: async (data: any) => {
    const response = await fetch(`${CONFIG.API_BASE_URL}${API_PREFIX}/payments/initiate/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  verify: async (ref: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/payments/verify/`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ref }) }
    );
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
  invoices: async (studentId: string) => {
    const response = await fetch(
      `${CONFIG.API_BASE_URL}${API_PREFIX}/invoices/?student_id=${studentId}`
    );
    if (response.ok) return { success: true, data: await response.json() };
    return { success: false };
  },
};

// EXPORT ALL - Mobile matched to Frontend + Backend
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
  // NEW MODULES - 100% matches frontend/backend
  admission: admissionApi,
  transcript: transcriptApi,
  hostel: hostelApi,
  clearance: clearanceApi,
  siwes: siwesApi,
  alumni: alumniApi,
  lib: libApi,
  calendar: calendarApi,
  leave: leaveApi,
  idCard: idCardApi,
  notification: notificationApi,
  payment: paymentApi,
};

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
// HELPERS - Secure Token & Offline Support
// ============================================================

async function getToken(): Promise<string | null> {
  try {
    const { getToken: getStoredToken } = await import('./storage');
    return await getStoredToken();
  } catch {
    return null;
  }
}

// ============================================================
// API CLIENT WITH OFFLINE SUPPORT
// ============================================================

interface APIRequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: object;
  headers?: Record<string, string>;
  useOfflineQueue?: boolean;  // Queue request if offline
  useCache?: boolean;     // Use cached response if available
  cacheTTL?: number;     // Cache TTL in ms (default 5 min)
  retries?: number;    // Max retries (default 3)
  retryDelay?: number;  // Delay between retries (default 1000ms)
}

interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  cached?: boolean;
}

// Create API client with offline support
export function createAPIClient(baseURL: string, prefix: string) {
  return {
    async request<T = any>(
      endpoint: string,
      config: APIRequestConfig = {}
    ): Promise<APIResponse<T>> {
      const {
        method = 'GET',
        body,
        headers = {},
        useOfflineQueue = false,
        useCache = false,
        cacheTTL = 300000,  // 5 min
        retries = 3,
        retryDelay = 1000,
      } = config;

      const url = `${baseURL}${prefix}${endpoint}`;
      const token = await getToken();
      
      // Add auth header if available
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      headers['Content-Type'] = 'application/json';

      // Check cache for GET requests
      if (useCache && method === 'GET') {
        const { getCache: getCached } = await import('./storage');
        const cached = await getCached(endpoint);
        if (cached) {
          return { success: true, data: cached, cached: true };
        }
      }

      // Try online request with retries
      let lastError: Error | null = null;
      for (let attempt = 0; attempt < retries; attempt++) {
        try {
          const response = await fetch(url, {
            method,
            body: body ? JSON.stringify(body) : undefined,
            headers,
          });

          if (response.ok) {
            const data = await response.json();
            
            // Cache successful GET responses
            if (useCache && method === 'GET') {
              const { setCache: setCached } = await import('./storage');
              await setCached(endpoint, data, cacheTTL);
            }
            
            return { success: true, data };
          }
          
          // Handle 401 - token expired
          if (response.status === 401) {
            // TODO: Implement token refresh
            return { success: false, error: 'Session expired' };
          }
          
          const errorData = await response.json().catch(() => ({}));
          return { success: false, error: errorData.error || 'Request failed' };
        } catch (e) {
          lastError = e as Error;
          
          // Check if offline
          const { isOnline } = await import('./storage');
          const online = await isOnline();
          
          if (!online) {
            // Queue for offline if enabled
            if (useOfflineQueue && method !== 'GET') {
              const { queueOfflineRequest } = await import('./storage');
              await queueOfflineRequest({
                id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                method,
                url: endpoint,
                data: body,
                timestamp: Date.now(),
              });
              return { success: false, error: 'queued' };
            }
            return { success: false, error: 'No internet connection' };
          }
          
          // Wait before retry
          if (attempt < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1));
          }
        }
      }

      return { success: false, error: lastError?.message || 'Request failed' };
    },

    // Convenience methods
    get<T = any>(endpoint: string, config?: APIRequestConfig): Promise<APIResponse<T>> {
      return this.request<T>(endpoint, { ...config, method: 'GET' });
    },
    post<T = any>(endpoint: string, body: object, config?: APIRequestConfig): Promise<APIResponse<T>> {
      return this.request<T>(endpoint, { ...config, method: 'POST', body });
    },
    put<T = any>(endpoint: string, body: object, config?: APIRequestConfig): Promise<APIResponse<T>> {
      return this.request<T>(endpoint, { ...config, method: 'PUT', body });
    },
    patch<T = any>(endpoint: string, body: object, config?: APIRequestConfig): Promise<APIResponse<T>> {
      return this.request<T>(endpoint, { ...config, method: 'PATCH', body });
    },
    delete<T = any>(endpoint: string, config?: APIRequestConfig): Promise<APIResponse<T>> {
      return this.request<T>(endpoint, { ...config, method: 'DELETE' });
    },
  };
}

// Create the API client instance
export const api = createAPIClient(BASE_URL, API_PREFIX);

// Export all APIs with offline support
export default {
  auth: authApi,
  student: studentApi,
  academic: academicApi,
  staff: staffApi,
  learning: learningApi,
  hostel: hostelApi,
  client: api,
};
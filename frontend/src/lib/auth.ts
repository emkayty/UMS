/**
 * UMS Frontend - Auth Module
 * Authentication utilities and hooks
 */

import { authApi } from './api';

// Token management
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('ums_token');
}

export function setToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('ums_token', token);
}

export function clearToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('ums_token');
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

// User management
export interface User {
  id?: number | string;
  email?: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  [key: string]: any;
}

export function getUser(): User | null {
  if (typeof window === 'undefined') return null;
  const user = localStorage.getItem('ums_user');
  return user ? JSON.parse(user) : null;
}

export function setUser(user: User): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('ums_user', JSON.stringify(user));
}

export function clearUser(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('ums_user');
}

// Logout
export async function logout(): Promise<void> {
  try {
    await authApi.logout();
  } catch {
    // Ignore errors
  }
  clearToken();
  clearUser();
}

// Protect route - redirect to login if not authenticated
export function requireAuth(): boolean {
  if (!isAuthenticated()) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    return false;
  }
  return true;
}

// Check role
export function hasRole(requiredRole: string): boolean {
  const user = getUser();
  if (!user) return false;
  return (user as any).role === requiredRole;
}

// Hook for auth state
export function useAuth() {
  const user = getUser();
  return {
    token: getToken(),
    user: user as any,
    isAuthenticated: isAuthenticated(),
    logout,
  };
}

// Default export
export default {
  getToken,
  setToken,
  clearToken,
  isAuthenticated,
  getUser,
  setUser,
  clearUser,
  logout,
  requireAuth,
  hasRole,
  useAuth,
};
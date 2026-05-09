/**
 * UMS Mobile - Secure Storage Service
 * Enterprise-grade secure storage with encrypted token handling
 */

import AsyncStorage from "@react-native-async-storage/async-storage";

// Try to use secure storage - fall back to encrypted AsyncStorage
let SecureStorage: any = null;
let hasSecureStorage = false;

try {
  // Try expo-secure-store first (Expo managed)
  SecureStorage = require('expo-secure-store');
  hasSecureStorage = true;
} catch {
  try {
    // Try react-native-keychain (bare workflow)
    SecureStorage = require('react-native-keychain');
    hasSecureStorage = true;
  } catch {
    // Fall back to encrypted AsyncStorage
    SecureStorage = null;
    hasSecureStorage = false;
  }
}

const STORAGE_KEYS = {
  USER: "@ums_user",
  TOKEN: "@ums_token",  // Will use secure storage
  REFRESH_TOKEN: "@ums_refresh_token",  // Will use secure storage
  SETTINGS: "@ums_settings",
  CACHE: "@ums_cache",
  OFFLINE_QUEUE: "@ums_offline_queue",
};

// Encryption key for fallback (in production, use device-specific key)
const ENCRYPTION_KEY = "ums_secure_key_v1";

// Buffer polyfill for React Native
const Buffer = require('buffer').Buffer;

/**
 * Simple XOR encryption for fallback (not secure, but better than plain)
 * In production, use proper encryption library
 */
function encrypt(data: string): string {
  let result = "";
  for (let i = 0; i < data.length; i++) {
    result += String.fromCharCode(
      data.charCodeAt(i) ^ ENCRYPTION_KEY.charCodeAt(i % ENCRYPTION_KEY.length)
    );
  }
  return Buffer.from(result, 'binary').toString('base64');
}

function decrypt(data: string): string {
  try {
    const decoded = Buffer.from(data, 'base64').toString('binary');
    let result = "";
    for (let i = 0; i < decoded.length; i++) {
      result += String.fromCharCode(
        decoded.charCodeAt(i) ^ ENCRYPTION_KEY.charCodeAt(i % ENCRYPTION_KEY.length)
      );
    }
    return result;
  } catch {
    return data;
  }
}

/**
 * Check if secure storage is available
 */
export function hasSecureStorageDevice(): boolean {
  return hasSecureStorage;
}

// ============================================================
// USER STORAGE (Non-sensitive)
// ============================================================

export async function saveUser(user: object): Promise<void> {
  await AsyncStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

export async function getUser(): Promise<object | null> {
  const data = await AsyncStorage.getItem(STORAGE_KEYS.USER);
  return data ? JSON.parse(data) : null;
}

export async function clearUser(): Promise<void> {
  await AsyncStorage.removeItem(STORAGE_KEYS.USER);
}

// ============================================================
// SECURE TOKEN STORAGE (Sensitive - uses encrypted storage)
// ============================================================

export async function saveToken(token: string): Promise<void> {
  if (hasSecureStorage && SecureStorage) {
    try {
      // Use expo-secure-store
      if (SecureStorage.setItemAsync) {
        await SecureStorage.setItemAsync(STORAGE_KEYS.TOKEN, token, {
          keychainService: 'ums_tokens',
        });
        return;
      }
      // Use react-native-keychain
      if (SecureStorage.setPassword) {
        await SecureStorage.setPassword({
          service: 'ums_tokens',
          password: token,
        });
        return;
      }
    } catch {
      // Fall through to encrypted storage
    }
  }
  
  // Fall back to encrypted AsyncStorage
  const encrypted = encrypt(token);
  await AsyncStorage.setItem(STORAGE_KEYS.TOKEN, encrypted);
}

export async function getToken(): Promise<string | null> {
  if (hasSecureStorage && SecureStorage) {
    try {
      // Use expo-secure-store
      if (SecureStorage.getItemAsync) {
        const token = await SecureStorage.getItemAsync(STORAGE_KEYS.TOKEN, {
          keychainService: 'ums_tokens',
        });
        if (token) return token;
      }
      // Use react-native-keychain
      if (SecureStorage.getPassword) {
        const result = await SecureStorage.getPassword({
          service: 'ums_tokens',
        });
        if (result) return result.password;
      }
    } catch {
      // Fall through to encrypted storage
    }
  }
  
  // Fall back to encrypted AsyncStorage
  const encrypted = await AsyncStorage.getItem(STORAGE_KEYS.TOKEN);
  if (!encrypted) return null;
  
  try {
    return decrypt(encrypted);
  } catch {
    return null;
  }
}

export async function clearToken(): Promise<void> {
  if (hasSecureStorage && SecureStorage) {
    try {
      // Use expo-secure-store
      if (SecureStorage.deleteItemAsync) {
        await SecureStorage.deleteItemAsync(STORAGE_KEYS.TOKEN, {
          keychainService: 'ums_tokens',
        });
      }
      // Use react-native-keychain
      if (SecureStorage.resetPassword) {
        await SecureStorage.resetPassword({
          service: 'ums_tokens',
        });
      }
    } catch {
      // Fall through
    }
  }
  
  // Also clear from AsyncStorage
  await AsyncStorage.removeItem(STORAGE_KEYS.TOKEN);
}

// ============================================================
// REFRESH TOKEN (Highly Sensitive)
// ============================================================

export async function saveRefreshToken(token: string): Promise<void> {
  if (hasSecureStorage && SecureStorage) {
    try {
      if (SecureStorage.setItemAsync) {
        await SecureStorage.setItemAsync(STORAGE_KEYS.REFRESH_TOKEN, token, {
          keychainService: 'ums_tokens',
        });
        return;
      }
      if (SecureStorage.setPassword) {
        await SecureStorage.setPassword({
          service: 'ums_refresh',
          password: token,
        });
        return;
      }
    } catch {}
  }
  
  const encrypted = encrypt(token);
  await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, encrypted);
}

export async function getRefreshToken(): Promise<string | null> {
  if (hasSecureStorage && SecureStorage) {
    try {
      if (SecureStorage.getItemAsync) {
        const token = await SecureStorage.getItemAsync(STORAGE_KEYS.REFRESH_TOKEN, {
          keychainService: 'ums_tokens',
        });
        if (token) return token;
      }
      if (SecureStorage.getPassword) {
        const result = await SecureStorage.getPassword({
          service: 'ums_refresh',
        });
        if (result) return result.password;
      }
    } catch {}
  }
  
  const encrypted = await AsyncStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  if (!encrypted) return null;
  
  try {
    return decrypt(encrypted);
  } catch {
    return null;
  }
}

export async function clearRefreshToken(): Promise<void> {
  if (hasSecureStorage && SecureStorage) {
    try {
      if (SecureStorage.deleteItemAsync) {
        await SecureStorage.deleteItemAsync(STORAGE_KEYS.REFRESH_TOKEN, {
          keychainService: 'ums_tokens',
        });
      }
    } catch {}
  }
  
  await AsyncStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
}

// ============================================================
// SETTINGS STORAGE (Non-sensitive)
// ============================================================

export async function saveSettings(settings: object): Promise<void> {
  await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
}

export async function getSettings(): Promise<object | null> {
  const data = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
  return data ? JSON.parse(data) : null;
}

// ============================================================
// GENERIC CACHE (Non-sensitive)
// ============================================================

export async function setCache(key: string, data: object, ttl: number = 3600000): Promise<void> {
  const cacheData = { data, timestamp: Date.now(), ttl };
  await AsyncStorage.setItem(`${STORAGE_KEYS.CACHE}_${key}`, JSON.stringify(cacheData));
}

export async function getCache(key: string): Promise<object | null> {
  const data = await AsyncStorage.getItem(`${STORAGE_KEYS.CACHE}_${key}`);
  if (!data) return null;
  
  const { data: cached, timestamp, ttl } = JSON.parse(data);
  if (Date.now() - timestamp > ttl) {
    await AsyncStorage.removeItem(`${STORAGE_KEYS.CACHE}_${key}`);
    return null;
  }
  return cached;
}

// ============================================================
// OFFLINE QUEUE (Non-sensitive)
// ============================================================

export interface OfflineRequest {
  id: string;
  method: string;
  url: string;
  data?: object;
  timestamp: number;
}

export async function queueOfflineRequest(request: OfflineRequest): Promise<void> {
  const queue = await getOfflineQueue();
  queue.push(request);
  await AsyncStorage.setItem(STORAGE_KEYS.OFFLINE_QUEUE, JSON.stringify(queue));
}

export async function getOfflineQueue(): Promise<OfflineRequest[]> {
  const data = await AsyncStorage.getItem(STORAGE_KEYS.OFFLINE_QUEUE);
  return data ? JSON.parse(data) : [];
}

export async function clearOfflineQueue(): Promise<void> {
  await AsyncStorage.removeItem(STORAGE_KEYS.OFFLINE_QUEUE);
}

export async function removeFromOfflineQueue(id: string): Promise<void> {
  const queue = await getOfflineQueue();
  const filtered = queue.filter((r) => r.id !== id);
  await AsyncStorage.setItem(STORAGE_KEYS.OFFLINE_QUEUE, JSON.stringify(filtered));
}

// ============================================================
// CLEAR ALL (includes secure storage)
// ============================================================

export async function clearAllStorage(): Promise<void> {
  // Clear AsyncStorage
  const keys = Object.values(STORAGE_KEYS);
  await AsyncStorage.multiRemove(keys);
  
  // Clear secure storage
  await clearToken();
  await clearRefreshToken();
}

// ============================================================
// NETWORK STATUS
// ============================================================

export async function isOnline(): Promise<boolean> {
  try {
    const NetInfo = require('@react-native-community/netinfo');
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  } catch {
    // Fall back to react-native
    try {
      const { NetInfo: RNNetInfo } = require('react-native');
      const state = await RNNetInfo.fetch();
      return state.isConnected ?? false;
    } catch {
      // Default to online if can't determine
      return true;
    }
  }
}
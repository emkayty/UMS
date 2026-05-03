import AsyncStorage from "@react-native-async-storage/async-storage";

const STORAGE_KEYS = {
  USER: "@ums_user",
  TOKEN: "@ums_token",
  SETTINGS: "@ums_settings",
  CACHE: "@ums_cache",
  OFFLINE_QUEUE: "@ums_offline_queue",
};

// User Storage
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

// Token Storage
export async function saveToken(token: string): Promise<void> {
  await AsyncStorage.setItem(STORAGE_KEYS.TOKEN, token);
}

export async function getToken(): Promise<string | null> {
  return AsyncStorage.getItem(STORAGE_KEYS.TOKEN);
}

export async function clearToken(): Promise<void> {
  await AsyncStorage.removeItem(STORAGE_KEYS.TOKEN);
}

// Settings Storage
export async function saveSettings(settings: object): Promise<void> {
  await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
}

export async function getSettings(): Promise<object | null> {
  const data = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
  return data ? JSON.parse(data) : null;
}

// Generic Cache
export async function setCache(key: string, data: object, ttl: number = 3600000): Promise<void> {
  const cacheData = { data, timestamp: Date.now(), ttl };
  await AsyncStorage.setItem(`${STORAGE_KEYS_CACHE}_${key}`, JSON.stringify(cacheData));
}

export async function getCache(key: string): Promise<object | null> {
  const data = await AsyncStorage.getItem(`${STORAGE_KEYS_CACHE}_${key}`);
  if (!data) return null;
  
  const { data: cached, timestamp, ttl } = JSON.parse(data);
  if (Date.now() - timestamp > ttl) {
    await AsyncStorage.removeItem(`${STORAGE_KEYS_CACHE}_${key}`);
    return null;
  }
  return cached;
}

// Offline Queue for API requests
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

// Clear All
export async function clearAllStorage(): Promise<void> {
  const keys = Object.values(STORAGE_KEYS);
  await AsyncStorage.multiRemove(keys);
}

// Check Online Status
export async function isOnline(): Promise<boolean> {
  try {
    const netInfo = await import("react-native").then((m) => m.NetInfo);
    const state = await netInfo.fetch();
    return state.isConnected ?? false;
  } catch {
    return true;
  }
}
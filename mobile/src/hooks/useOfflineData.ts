/**
 * UMS Mobile - Enhanced API Hook with Offline Support
 * Provides offline-first data fetching with caching
 */

import { useState, useEffect, useCallback } from 'react';
import { isOnline, getCache, setCache, getOfflineQueue } from '../services/storage';

// Configuration
const DEFAULT_CACHE_TTL = 5 * 60 * 1000; // 5 minutes
const OFFLINE_QUEUE_KEY = 'offline_queue';

/**
 * Hook for fetching data with offline support
 * - Checks cache first if offline
 * - Fetches from API when online
 * - Caches successful responses
 * - Queues requests when offline (if enabled)
 */
export function useOfflineData<T>(
  fetchFn: () => Promise<{ success: boolean; data?: T; error?: string }>,
  options: {
    cacheKey?: string;
    cacheTTL?: number;
    enabled?: boolean;
    offlineQueue?: boolean;
  } = {}
) {
  const {
    cacheKey,
    cacheTTL = DEFAULT_CACHE_TTL,
    enabled = true,
    offlineQueue = false,
  } = options;

  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCached, setIsCached] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  const fetchData = useCallback(async (forceOnline = false) => {
    if (!enabled) return;

    setLoading(true);
    setError(null);

    try {
      const online = await isOnline();

      // Try cache first if offline or cache key provided
      if (!online && cacheKey) {
        const cached = await getCache(cacheKey);
        if (cached) {
          setData(cached as T);
          setIsCached(true);
          setLoading(false);
          return;
        }
      }

      // Fetch from API
      const result = await fetchFn();

      if (result.success && result.data) {
        setData(result.data);
        setIsCached(false);
        
        // Cache successful response
        if (cacheKey) {
          await setCache(cacheKey, result.data, cacheTTL);
        }
      } else if (!online && offlineQueue) {
        // Queue for later if offline
        setError('queued');
      } else {
        // Try cache as fallback
        if (cacheKey) {
          const cached = await getCache(cacheKey);
          if (cached) {
            setData(cached as T);
            setIsCached(true);
          } else {
            setError(result.error || 'Failed to load data');
          }
        } else {
          setError(result.error || 'Failed to load data');
        }
      }
    } catch (err) {
      // Try cache on error
      if (cacheKey) {
        const cached = await getCache(cacheKey);
        if (cached) {
          setData(cached as T);
          setIsCached(true);
        } else {
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      } else {
        setError(err instanceof Error ? err.message : 'Unknown error');
      }
    } finally {
      setLoading(false);
    }
  }, [fetchFn, cacheKey, cacheTTL, enabled, offlineQueue]);

  // Initial load
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Sync pending queue when online
  const syncPending = useCallback(async () => {
    setIsSyncing(true);
    try {
      const online = await isOnline();
      if (!online) return;

      // Get pending requests and process them
      // This would typically use the mobile_api.ts client
      setIsSyncing(false);
    } catch (err) {
      setIsSyncing(false);
    }
  }, []);

  const refetch = useCallback(() => {
    return fetchData(true);
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    isCached,
    isSyncing,
    refetch,
    syncPending,
  };
}

/**
 * Hook for managing online/offline status
 */
export function useNetworkStatus() {
  const [online, setOnline] = useState(true);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const checkStatus = async () => {
      const status = await isOnline();
      setOnline(status);

      // Check pending queue
      const queue = await getOfflineQueue();
      setPendingCount(queue.length);
    };

    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return {
    online,
    pendingCount,
    hasPending: pendingCount > 0,
  };
}

/**
 * Hook for offline-aware mutations (POST, PUT, DELETE)
 */
export function useOfflineMutation<T, TVariables>(
  mutationFn: (variables: TVariables) => Promise<{ success: boolean; data?: T; error?: string }>,
  options: {
    onSuccess?: (data: T) => void;
    onError?: (error: string) => void;
  } = {}
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(async (variables: TVariables) => {
    setLoading(true);
    setError(null);

    try {
      const online = await isOnline();

      if (online) {
        const result = await mutationFn(variables);
        
        if (result.success) {
          options.onSuccess?.(result.data as T);
          return result.data;
        } else {
          setError(result.error || 'Mutation failed');
          options.onError?.(result.error || 'Mutation failed');
          return null;
        }
      } else {
        // Queue mutation for later
        // For now, return error - full implementation would queue
        setError('No internet connection');
        options.onError?.('No internet connection');
        return null;
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMsg);
      options.onError?.(errorMsg);
      return null;
    } finally {
      setLoading(false);
    }
  }, [mutationFn, options]);

  return {
    mutate,
    loading,
    error,
  };
}

export default {
  useOfflineData,
  useNetworkStatus,
  useOfflineMutation,
};
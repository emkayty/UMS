import { useEffect, useState, useCallback } from "react";
import { NetInfo } from "react-native";
import { queueOfflineRequest, getOfflineQueue, removeFromOfflineQueue, isOnline, getCache, setCache } from "../services/storage";

interface UseOfflineOptions {
  autoSync?: boolean;
  syncInterval?: number;
}

export function useOfflineSync<T>(
  fetchOnline: () => Promise<T>,
  options: UseOfflineOptions = {}
) {
  const { autoSync = true, syncInterval = 30000 } = options;
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);

  const sync = useCallback(async () => {
    if (!(await isOnline())) return;
    
    setIsSyncing(true);
    try {
      const queue = await getOfflineQueue();
      for (const request of queue) {
        try {
          await fetch(request.url, {
            method: request.method,
            body: request.data ? JSON.stringify(request.data) : undefined,
            headers: { "Content-Type": "application/json" },
          });
          await removeFromOfflineQueue(request.id);
        } catch (e) {
          console.error("Sync failed:", request.id, e);
        }
      }
    } finally {
      setIsSyncing(false);
    }
  }, []);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchOnline();
      setData(result);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, [fetchOnline]);

  useEffect(() => {
    let mounted = true;
    let interval: ReturnType<typeof setInterval>;

    const init = async () => {
      if (await isOnline()) {
        await refetch();
      }
      if (autoSync) {
        interval = setInterval(sync, syncInterval);
      }
    };

    init();

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [refetch, sync, autoSync, syncInterval]);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(async (state) => {
      if (state.isConnected && autoSync) {
        await sync();
      }
    });
    return unsubscribe;
  }, [sync, autoSync]);

  return { data, loading, error, isSyncing, refetch, sync };
}

// Sync status hook
export function useSyncStatus() {
  const [online, setOnline] = useState(true);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const check = async () => {
      setOnline(await isOnline());
      const queue = await getOfflineQueue();
      setPendingCount(queue.length);
    };
    check();
    const interval = setInterval(check, 5000);
    return () => clearInterval(interval);
  }, []);

  return { online, pendingCount, needsSync: pendingCount > 0 };
}
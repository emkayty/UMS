/**
 * UMS Mobile - Push Notification Service
 * Handles FCM and Expo Push Notifications
 */

import { Platform } from 'react-native';
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

// Configure push notification behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});

/**
 * Push notification permission status
 */
export type PermissionStatus = 'granted' | 'denied' | 'undetermined';

/**
 * Initialize push notifications
 * Call this on app startup
 */
export async function initPushNotifications(): Promise<PermissionStatus> {
  // Check if running on device
  if (!Device.isDevice) {
    console.log('Push notifications not supported on simulator');
    return 'denied';
  }

  // Request permissions
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    console.log('Push notification permission not granted');
    return 'denied';
  }

  // Set notification channel for Android
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'Default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#1e40af',
    });

    // Create channels for different types
    await Notifications.setNotificationChannelAsync('alerts', {
      name: 'Alerts',
      importance: Notifications.AndroidImportance.HIGH,
      sound: 'default',
    });

    await Notifications.setNotificationChannelAsync('messages', {
      name: 'Messages',
      importance: Notifications.AndroidImportance.DEFAULT,
      sound: 'default',
    });

    await Notifications.setNotificationChannelAsync('reminders', {
      name: 'Reminders',
      importance: Notifications.AndroidImportance.DEFAULT,
    });
  }

  return 'granted';
}

/**
 * Get device push token for sending notifications
 * Send this to your backend
 */
export async function getPushToken(): Promise<string | null> {
  try {
    const { data: token } = await Notifications.getExpoPushTokenAsync({
      experienceId: 'ums-mobile',
    });
    return token;
  } catch (error) {
    console.error('Error getting push token:', error);
    return null;
  }
}

/**
 * Schedule a local notification
 */
export async function scheduleNotification(options: {
  title: string;
  body: string;
  data?: Record<string, any>;
  scheduledAt?: Date;
}): Promise<string | null> {
  try {
    const id = await Notifications.scheduleNotificationAsync({
      content: {
        title: options.title,
        body: options.body,
        data: options.data || {},
        sound: 'default',
      },
      trigger: options.scheduledAt || null,
    });
    return id;
  } catch (error) {
    console.error('Error scheduling notification:', error);
    return null;
  }
}

/**
 * Send local notification immediately
 */
export async function sendLocalNotification(options: {
  title: string;
  body: string;
  data?: Record<string, any>;
}): Promise<void> {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: options.title,
      body: options.body,
      data: options.data || {},
      sound: 'default',
    },
    trigger: null, // Send immediately
  });
}

/**
 * Cancel a scheduled notification
 */
export async function cancelNotification(id: string): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(id);
}

/**
 * Cancel all scheduled notifications
 */
export async function cancelAllNotifications(): Promise<void> {
  await Notifications.cancelAllScheduledNotificationsAsync();
}

/**
 * Get all scheduled notifications
 */
export async function getScheduledNotifications(): Promise<Notifications.NotificationRequest[]> {
  return await Notifications.getAllScheduledNotificationsAsync();
}

/**
 * Add notification response listener
 */
export function addNotificationResponseListener(
  callback: (response: Notifications.NotificationResponse) => void
): Notifications.Subscription {
  return Notifications.addNotificationResponseReceivedListener(callback);
}

/**
 * Add notification received listener
 */
export function addNotificationReceivedListener(
  callback: (notification: Notifications.Notification) => void
): Notifications.Subscription {
  return Notifications.addNotificationReceivedListener(callback);
}

/**
 * Remove all notification listeners
 */
export function removeNotificationListeners(): void {
  Notifications.removeAllNotificationListeners();
}

/**
 * Set badge count
 */
export async function setBadgeCount(count: number): Promise<void> {
  await Notifications.setBadgeCountAsync(count);
}

/**
 * Get badge count
 */
export async function getBadgeCount(): Promise<number> {
  return await Notifications.getBadgeCountAsync();
}

/**
 * Predefined notification helpers for common university events
 */

export const NotificationHelpers = {
  // New result available
  async resultPublished(resultId: string, courseName: string) {
    return sendLocalNotification({
      title: '📊 Result Published',
      body: `Your ${courseName} result is now available`,
      data: { type: 'result', resultId },
    });
  },

  // Fee reminder
  async feeDueReminder(amount: string, dueDate: string) {
    return sendLocalNotification({
      title: '💰 Fee Reminder',
      body: `Fee payment of ₦${amount} is due on ${dueDate}`,
      data: { type: 'fee_reminder' },
    });
  },

  // Course registration deadline
  async registrationDeadline(deadline: string) {
    return sendLocalNotification({
      title: '⚠️ Registration Deadline',
      body: `Course registration closes on ${deadline}`,
      data: { type: 'registration' },
    });
  },

  // Attendance alert
  async attendanceAlert(courseName: string, status: string) {
    return sendLocalNotification({
      title: '📢 Attendance Alert',
      body: `${courseName}: ${status}`,
      data: { type: 'attendance' },
    });
  },

  // Library due
  async libraryDue(bookTitle: string, dueDate: string) {
    return sendLocalNotification({
      title: '📚 Library Reminder',
      body: `"${bookTitle}" is due on ${dueDate}`,
      data: { type: 'library' },
    });
  },

  // Hostel assignment
  async hostelAssigned(roomNumber: string, hostelName: string) {
    return sendLocalNotification({
      title: '🏠 Hostel Assigned',
      body: `Room ${roomNumber} at ${hostelName}`,
      data: { type: 'hostel' },
    });
  },

  // AI response
  async aiResponse(question: string) {
    return sendLocalNotification({
      title: '🤖 AI Response Ready',
      body: `Your question has been answered`,
      data: { type: 'ai' },
    });
  },
};

export default {
  initPushNotifications,
  getPushToken,
  scheduleNotification,
  sendLocalNotification,
  cancelNotification,
  cancelAllNotifications,
  getScheduledNotifications,
  addNotificationResponseListener,
  addNotificationReceivedListener,
  removeNotificationListeners,
  setBadgeCount,
  getBadgeCount,
  NotificationHelpers,
};
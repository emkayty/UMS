/**
 * UMS Mobile - Screen Exports
 * All mobile screens - dynamically like frontend
 */

// Auth Screens
export { default as LoginScreen } from './LoginScreen';

// Main Screens
export { default as DashboardScreen } from './DashboardScreen';
export { default as AttendanceScreen } from './AttendanceScreen';
export { default as FinanceScreen } from './FinanceScreen';
export { default as ProfileScreen } from './ProfileScreen';
export { default as ResultsScreen } from './ResultsScreen';

// Extended Screens (matching frontend)
export { default as AIScreen } from './AIScreen';
export { default as CoursesScreen } from './CoursesScreen';
export { default as StaffScreen } from './StaffScreen';
export { default as LibraryScreen } from './LibraryScreen';

// Screen Types
export type AuthScreen = 'Login';
export type MainScreen = 'Dashboard' | 'Attendance' | 'Finance' | 'Profile' | 'Results';
export type ExtendedScreen = 'AI' | 'Courses' | 'Staff' | 'Library';

// All Screens Map
export const SCREENS = {
  // Auth
  Login: 'LoginScreen',
  
  // Main
  Dashboard: 'DashboardScreen',
  Attendance: 'AttendanceScreen',
  Finance: 'FinanceScreen',
  Profile: 'ProfileScreen',
  Results: 'ResultsScreen',
  
  // Extended
  AI: 'AIScreen',
  Courses: 'CoursesScreen',
  Staff: 'StaffScreen',
  Library: 'LibraryScreen',
} as const;

// Screen Categories
export const SCREEN_CATEGORIES = {
  AUTH: ['Login'],
  MAIN: ['Dashboard', 'Attendance', 'Finance', 'Profile', 'Results'],
  EXTENDED: ['AI', 'Courses', 'Staff', 'Library'],
} as const;

// Navigation Config
export const NAVIGATION_CONFIG = {
  initialRoute: 'Dashboard',
  authRequired: ['Dashboard', 'Attendance', 'Finance', 'Profile', 'Results', 'Courses', 'Staff', 'Library', 'AI'],
  bottomTabs: ['Dashboard', 'Attendance', 'Finance', 'Profile'],
} as const;
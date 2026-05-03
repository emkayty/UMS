import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createBottomTabNavigator, createNativeStackNavigator } from '@react-navigation/native-stack'
import { Ionicons } from '@expo/vector-icons'

// Screens - Dynamic import like frontend
import {
  DashboardScreen,
  ResultsScreen,
  AttendanceScreen,
  FinanceScreen,
  ProfileScreen,
  AIScreen,
  CoursesScreen,
  StaffScreen,
  LibraryScreen,
  LoginScreen,
  SCREENS,
  NAVIGATION_CONFIG,
} from './src/screens'

const Tab = createBottomTabNavigator()
const Stack = createNativeStackNavigator()

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap = 'home'
          if (route.name === 'Dashboard') iconName = 'home'
          else if (route.name === 'AI') iconName = 'bulb'
          else if (route.name === 'Courses') iconName = 'book'
          else if (route.name === 'Attendance') iconName = 'qr-code'
          else if (route.name === 'Finance') iconName = 'wallet'
          else if (route.name === 'Profile') iconName = 'person'
          return <Ionicons name={iconName} size={size} color={color} />
        },
        tabBarActiveTintColor: '#1e40af',
        tabBarInactiveTintColor: '#9ca3af',
        headerStyle: { backgroundColor: '#1e40af' },
        headerTintColor: 'white',
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="AI" component={AIScreen} options={{ title: 'AI Assistant' }} />
      <Tab.Screen name="Courses" component={CoursesScreen} />
      <Tab.Screen name="Attendance" component={AttendanceScreen} />
      <Tab.Screen name="Finance" component={FinanceScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  )
}

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Main" 
          component={TabNavigator}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Staff" 
          component={StaffScreen}
          options={{ 
            title: 'Staff Directory',
            headerStyle: { backgroundColor: '#1e40af' },
            headerTintColor: 'white',
          }}
        />
        <Stack.Screen 
          name="Library" 
          component={LibraryScreen}
          options={{ 
            title: 'Library',
            headerStyle: { backgroundColor: '#1e40af' },
            headerTintColor: 'white',
          }}
        />
        <Stack.Screen 
          name="Login" 
          component={LoginScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App

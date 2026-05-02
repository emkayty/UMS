import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { Ionicons } from '@expo/vector-icons'

// Screens
import { DashboardScreen } from './src/screens/DashboardScreen'
import { ResultsScreen } from './src/screens/ResultsScreen'
import { AttendanceScreen } from './src/screens/AttendanceScreen'
import FinanceScreen from './src/screens/FinanceScreen'
import ProfileScreen from './src/screens/ProfileScreen'

const Tab = createBottomTabNavigator()

function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName: keyof typeof Ionicons.glyphMap = 'home'
            if (route.name === 'Dashboard') iconName = 'home'
            else if (route.name === 'Results') iconName = 'school'
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
        <Tab.Screen name="Results" component={ResultsScreen} />
        <Tab.Screen name="Attendance" component={AttendanceScreen} />
        <Tab.Screen name="Finance" component={FinanceScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  )
}

export default App

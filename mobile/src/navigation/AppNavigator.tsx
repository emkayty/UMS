import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { View, Text, StyleSheet } from "react-native";

import LoginScreen from "../screens/LoginScreen";
import DashboardScreen from "../screens/DashboardScreen";
import ProfileScreen from "../screens/ProfileScreen";
import CoursesScreen from "../screens/CoursesScreen";
import FinanceScreen from "../screens/FinanceScreen";
import AttendanceScreen from "../screens/AttendanceScreen";
import HostelScreen from "../screens/HostelScreen";
import LibraryScreen from "../screens/LibraryScreen";
import ResultsScreen from "../screens/ResultsScreen";
import StaffScreen from "../screens/StaffScreen";
import TranscriptScreen from "../screens/TranscriptScreen";
import AdmissionScreen from "../screens/AdmissionScreen";
import AIScreen from "../screens/AIScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Tab Icon Component
function TabIcon({ name, focused }: { name: string; focused: boolean }) {
  const icons: Record<string, string> = {
    Home: "🏠",
    Courses: "📚",
    Finance: "💰",
    More: "☰",
  };
  return (
    <View style={styles.tabIcon}>
      <Text style={{ fontSize: focused ? 24 : 20 }}>{icons[name] || "•"}</Text>
    </View>
  );
}

// Bottom Tab Navigator
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused }) => <TabIcon name={route.name} focused={focused} />,
        tabBarActiveTintColor: "#2563eb",
        tabBarInactiveTintColor: "#9ca3af",
        headerStyle: { backgroundColor: "#2563eb" },
        headerTintColor: "#fff",
      })}
    >
      <Tab.Screen name="Home" component={DashboardScreen} options={{ title: "Dashboard" }} />
      <Tab.Screen name="Courses" component={CoursesScreen} options={{ title: "My Courses" }} />
      <Tab.Screen name="Finance" component={FinanceScreen} options={{ title: "Payments" }} />
      <Tab.Screen 
        name="More" 
        component={ProfileScreen} 
        options={{ 
          title: "Profile",
          headerShown: false,
        }} 
      />
    </Tab.Navigator>
  );
}

// Main Stack Navigator
export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: "#2563eb" },
          headerTintColor: "#fff",
          headerTitleStyle: { fontWeight: "600" },
          animation: "slide_from_right",
        }}
      >
        <Stack.Screen 
          name="Login" 
          component={LoginScreen} 
          options={{ headerShown: false }} 
        />
        <Stack.Screen 
          name="Main" 
          component={MainTabs} 
          options={{ headerShown: false }} 
        />
        <Stack.Screen name="Attendance" component={AttendanceScreen} />
        <Stack.Screen name="Hostel" component={HostelScreen} />
        <Stack.Screen name="Library" component={LibraryScreen} />
        <Stack.Screen name="Results" component={ResultsScreen} />
        <Stack.Screen name="Staff" component={StaffScreen} />
        <Stack.Screen name="Transcript" component={TranscriptScreen} />
        <Stack.Screen name="Admission" component={AdmissionScreen} />
        <Stack.Screen name="AI" component={AIScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  tabIcon: {
    alignItems: "center",
    justifyContent: "center",
  },
});

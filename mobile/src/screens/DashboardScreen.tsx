/**
 * Dashboard Screen
 * Main dashboard with stats and quick actions - API integrated
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { authApi, studentApi } from '../services/api';

interface Props {
  navigation: any;
}

export function DashboardScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      // Load user info
      const userRes = await authApi.me();
      if (userRes.success) {
        setUser(userRes.data);
      }

      // Load student profile
      const profileRes = await studentApi.profile();
      if (profileRes.success) {
        setProfile(profileRes.data);
      }
    } catch (error) {
      console.error('Load error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadDashboard();
  };

  // Stats from profile data
  const stats = [
    { label: 'GPA', value: profile?.cgpa || '0.0', color: '#22c55e', icon: 'school' },
    { label: 'Courses', value: profile?.current_courses || '0', color: '#3b82f6', icon: 'book' },
    { label: 'Due', value: profile?.fees_due || '0', color: '#f59e0b', icon: 'document-text' },
    { label: 'Msgs', value: profile?.unread_messages || '0', color: '#8b5cf6', icon: 'chatbubble' },
  ];

  // Quick actions
  const quickActions = [
    { label: 'Courses', icon: 'book', screen: 'Courses', color: '#3b82f6' },
    { label: 'Results', icon: 'school', screen: 'Results', color: '#22c55e' },
    { label: 'Attendance', icon: 'finger-print', screen: 'Attendance', color: '#f59e0b' },
    { label: 'Finance', icon: 'wallet', screen: 'Finance', color: '#8b5cf6' },
    { label: 'Library', icon: 'library', screen: 'Library', color: '#ec4899' },
    { label: 'Hostel', icon: 'home', screen: 'Hostel', color: '#f97316' },
  ];

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Welcome back,</Text>
          <Text style={styles.userName}>
            {user?.first_name || user?.name || 'Student'}
          </Text>
          <Text style={styles.level}>
            {profile?.current_level || '100'} Level
          </Text>
        </View>
        <TouchableOpacity onPress={() => navigation.navigate('Profile')}>
          <Ionicons name="person-circle" size={50} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Stats */}
      <View style={styles.statsContainer}>
        {stats.map((stat, index) => (
          <View key={index} style={styles.statCard}>
            <Ionicons name={stat.icon as any} size={20} color={stat.color} />
            <Text style={styles.statValue}>{stat.value}</Text>
            <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>

      {/* Quick Actions */}
      <Text style={styles.sectionTitle}>Quick Actions</Text>
      <View style={styles.actionsGrid}>
        {quickActions.map((action, index) => (
          <TouchableOpacity
            key={index}
            style={styles.actionCard}
            onPress={() => navigation.navigate(action.screen)}
          >
            <View style={[styles.actionIcon, { backgroundColor: action.color + '20' }]}>
              <Ionicons name={action.icon as any} size={24} color={action.color} />
            </View>
            <Text style={styles.actionLabel}>{action.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.version}>Version 2.0.0</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.gray[50],
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    backgroundColor: COLORS.primary,
    padding: 20,
    paddingTop: 50,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  greeting: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  level: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginHorizontal: 15,
    marginTop: 10,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 10,
  },
  actionCard: {
    width: '31%',
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 12,
    margin: 5,
    alignItems: 'center',
  },
  actionIcon: {
    width: 45,
    height: 45,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionLabel: {
    fontSize: 11,
    color: '#333',
    marginTop: 5,
  },
  version: {
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 30,
    color: '#999',
  },
});
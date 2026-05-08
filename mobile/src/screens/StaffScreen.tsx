/**
 * Staff Screen
 * Staff portal - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { staffApi } from '../services/api';

interface Props {
  navigation: any;
}

export function StaffScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);
  const [leaveBalance, setLeaveBalance] = useState<any>(null);

  useEffect(() => {
    loadStaff();
  }, []);

  const loadStaff = async () => {
    try {
      const profileRes = await staffApi.profile();
      if (profileRes.success) {
        setProfile(profileRes.data);
      }

      const leaveRes = await staffApi.leaveBalance();
      if (leaveRes.success) {
        setLeaveBalance(leaveRes.data);
      }
    } catch (error) {
      console.error('Load staff error:', error);
    } finally {
      setLoading(false);
    }
  };

  const menuItems = [
    { icon: 'people', label: 'Students', screen: 'Students', color: '#3b82f6' },
    { icon: 'book', label: 'Courses', screen: 'Courses', color: '#22c55e' },
    { icon: 'document-text', label: 'Results', screen: 'Results', color: '#f59e0b' },
    { icon: 'calendar', label: 'Attendance', screen: 'Attendance', color: '#8b5cf6' },
    { icon: 'wallet', label: 'Payments', screen: 'Payments', color: '#ec4899' },
    { icon: 'school', label: 'Clearance', screen: 'Clearance', color: '#f97316' },
  ];

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Staff Portal</Text>
        <Text style={styles.headerSubtitle}>
          {profile?.title || 'Lecturer'} {profile?.name || ''}
        </Text>
      </View>

      {/* Quick Stats */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Ionicons name="calendar" size={24} color="#3b82f6" />
          <Text style={styles.statValue}>{leaveBalance?.days_left || 0}</Text>
          <Text style={styles.statLabel}>Leave Days</Text>
        </View>
        <View style={styles.statCard}>
          <Ionicons name="book" size={24} color="#22c55e" />
          <Text style={styles.statValue}>{profile?.courses || 0}</Text>
          <Text style={styles.statLabel}>Courses</Text>
        </View>
        <View style={styles.statCard}>
          <Ionicons name="people" size={24} color="#f59e0b" />
          <Text style={styles.statValue}>{profile?.students || 0}</Text>
          <Text style={styles.statLabel}>Students</Text>
        </View>
      </View>

      {/* Menu */}
      <ScrollView style={styles.content}>
        <Text style={styles.sectionTitle}>quick Access</Text>
        <View style={styles.menuGrid}>
          {menuItems.map((item, index) => (
            <TouchableOpacity key={index} style={styles.menuCard}>
              <View style={[styles.menuIcon, { backgroundColor: item.color + '20' }]}>
                <Ionicons name={item.icon as any} size={24} color={item.color} />
              </View>
              <Text style={styles.menuLabel}>{item.label}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Leave Section */}
        <Text style={styles.sectionTitle}>Leave Management</Text>
        <View style={styles.leaveCard}>
          <View style={styles.leaveRow}>
            <Text style={styles.leaveLabel}>Annual Leave</Text>
            <Text style={styles.leaveValue}>{leaveBalance?.annual || 0} days</Text>
          </View>
          <View style={styles.leaveRow}>
            <Text style={styles.leaveLabel}>Sick Leave</Text>
            <Text style={styles.leaveValue}>{leaveBalance?.sick || 0} days</Text>
          </View>
          <View style={styles.leaveRow}>
            <Text style={styles.leaveLabel}>Casual Leave</Text>
            <Text style={styles.leaveValue}>{leaveBalance?.casual || 0} days</Text>
          </View>
          <TouchableOpacity style={styles.requestLeaveButton}>
            <Text style={styles.requestLeaveText}>Request Leave</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
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
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  statsContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 12,
    padding: 15,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  content: {
    flex: 1,
    paddingHorizontal: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 15,
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  menuCard: {
    width: '31%',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 15,
  },
  menuIcon: {
    width: 45,
    height: 45,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  menuLabel: {
    fontSize: 12,
    color: '#333',
    marginTop: 8,
    textAlign: 'center',
  },
  leaveCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
  },
  leaveRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  leaveLabel: {
    fontSize: 14,
    color: '#666',
  },
  leaveValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  requestLeaveButton: {
    backgroundColor: COLORS.primary,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  requestLeaveText: {
    color: '#fff',
    fontWeight: '600',
  },
});
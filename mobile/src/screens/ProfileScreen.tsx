/**
 * Profile Screen
 * User profile and settings
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Image,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { authApi, studentApi } from '../services/api';

export function ProfileScreen() {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  
  useEffect(() => {
    loadProfile();
  }, []);
  
  const loadProfile = async () => {
    try {
      const userRes = await authApi.me();
      if (userRes.success) {
        setUser(userRes.data);
      }
      
      const profileRes = await studentApi.profile();
      if (profileRes.success) {
        setProfile(profileRes.data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  const menuItems = [
    { icon: 'person', label: 'Edit Profile', onPress: () => {} },
    { icon: 'notifications', label: 'Notifications', onPress: () => {} },
    { icon: 'lock-closed', label: 'Change Password', onPress: () => {} },
    { icon: 'globe', label: 'Language', onPress: () => {} },
    { icon: 'help-circle', label: 'Help & Support', onPress: () => {} },
    { icon: 'document-text', label: 'Terms & Privacy', onPress: () => {} },
    { icon: 'log-out', label: 'Logout', onPress: () => {}, danger: true },
  ];
  
  if (loading) {
    return (
      <View style={styles.centered}>
        <Text>Loading...</Text>
      </View>
    );
  }
  
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatarContainer}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {user?.first_name?.[0] || 'U'}
            </Text>
          </View>
        </View>
        <Text style={styles.name}>
          {user?.first_name} {user?.last_name}
        </Text>
        <Text style={styles.email}>{user?.email}</Text>
        <View style={styles.statusBadge}>
          <Text style={styles.statusText}>
            {profile?.status || 'Student'}
          </Text>
        </View>
      </View>
      
      {/* Quick Info */}
      <View style={styles.infoCard}>
        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Matric Number</Text>
          <Text style={styles.infoValue}>
            {profile?.matric_number || '-'}
          </Text>
        </View>
        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Level</Text>
          <Text style={styles.infoValue}>
            {profile?.current_level || '-'}
          </Text>
        </View>
        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Programme</Text>
          <Text style={styles.infoValue}>
            {profile?.programme || '-'}
          </Text>
        </View>
      </View>
      
      {/* Menu */}
      <View style={styles.menu}>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.menuItem}
            onPress={item.onPress}
          >
            <View style={styles.menuItemLeft}>
              <Ionicons
                name={item.icon as any}
                size={22}
                color={item.danger ? COLORS.error : COLORS.gray[700]}
              />
              <Text style={[
                styles.menuLabel,
                item.danger && { color: COLORS.error }
              ]}>
                {item.label}
              </Text>
            </View>
            <Ionicons
              name="chevron-forward"
              size={20}
              color={COLORS.gray[400]}
            />
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
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: COLORS.primary,
  },
  avatarContainer: {
    marginBottom: 15,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.white,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  name: {
    fontSize: 22,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  email: {
    fontSize: 14,
    color: COLORS.white,
    opacity: 0.8,
    marginTop: 4,
  },
  statusBadge: {
    marginTop: 10,
    backgroundColor: COLORS.accent,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: COLORS.white,
    fontSize: 12,
    fontWeight: '600',
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    margin: 15,
    padding: 15,
    borderRadius: 12,
  },
  infoItem: {
    flex: 1,
    alignItems: 'center',
  },
  infoLabel: {
    fontSize: 11,
    color: COLORS.gray[500],
    marginBottom: 4,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray[900],
  },
  menu: {
    backgroundColor: COLORS.white,
    marginHorizontal: 15,
    borderRadius: 12,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray[100],
  },
  menuItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuLabel: {
    fontSize: 15,
    color: COLORS.gray[700],
    marginLeft: 15,
  },
  version: {
    textAlign: 'center',
    marginTop: 30,
    marginBottom: 30,
    color: COLORS.gray[400],
    fontSize: 12,
  },
});
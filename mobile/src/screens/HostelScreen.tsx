/**
 * Hostel Screen
 * Hostel services - API integrated
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
import { hostelApi } from '../services/api';

interface Props {
  navigation: any;
}

export function HostelScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [application, setApplication] = useState<any>(null);
  const [allocation, setAllocation] = useState<any>(null);

  useEffect(() => {
    loadHostel();
  }, []);

  const loadHostel = async () => {
    try {
      const appResult = await hostelApi.applications();
      if (appResult.success) {
        setApplication(appResult.data);
      }

      const allocResult = await hostelApi.allocation();
      if (allocResult.success) {
        setAllocation(allocResult.data);
      }
    } catch (error) {
      console.error('Load hostel error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Hostel</Text>
        <Text style={styles.headerSubtitle}>Accommodation services</Text>
      </View>

      <ScrollView style={styles.content}>
        {/* Allocation Status */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Your Hostel</Text>
          {allocation ? (
            <>
              <View style={styles.infoRow}>
                <Text style={styles.infoLabel}>Hostel</Text>
                <Text style={styles.infoValue}>{allocation.hostel_name || 'N/A'}</Text>
              </View>
              <View style={styles.infoRow}>
                <Text style={styles.infoLabel}>Room</Text>
                <Text style={styles.infoValue}>{allocation.room_number || 'N/A'}</Text>
              </View>
              <View style={styles.infoRow}>
                <Text style={styles.infoLabel}>Bed</Text>
                <Text style={styles.infoValue}>{allocation.bed || 'N/A'}</Text>
              </View>
            </>
          ) : (
            <Text style={styles.noDataText}>No hostel allocation</Text>
          )}
        </View>

        {/* Application Status */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Application Status</Text>
          {application ? (
            <View style={styles.statusRow}>
              <Ionicons
                name={application.status === 'approved' ? 'checkmark-circle' : 'time'}
                size={24}
                color={application.status === 'approved' ? '#22c55e' : '#f59e0b'}
              />
              <Text style={styles.statusText}>
                {application.status === 'approved' ? 'Approved' : 
                 application.status === 'pending' ? 'Pending' : 'Not Applied'}
              </Text>
            </View>
          ) : (
            <Text style={styles.noDataText}>No active application</Text>
          )}
        </View>

        {/* Actions */}
        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="add-circle-outline" size={24} color="#fff" />
          <Text style={styles.actionButtonText}>Apply for Hostel</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]}>
          <Ionicons name="swap-horizontal-outline" size={24} color={COLORS.primary} />
          <Text style={[styles.actionButtonText, { color: COLORS.primary }]}>
            Request Room Change
          </Text>
        </TouchableOpacity>
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
  content: {
    flex: 1,
    padding: 15,
  },
  card: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 15,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  infoLabel: {
    fontSize: 14,
    color: '#666',
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  noDataText: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 16,
    marginLeft: 10,
    color: '#333',
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    padding: 15,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  secondaryButton: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 10,
  },
});
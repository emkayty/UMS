/**
 * Attendance Screen
 * Student attendance records - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { studentApi } from '../services/api';

interface Props {
  navigation: any;
}

interface Attendance {
  id: number;
  course_code: string;
  course_name: string;
  total: number;
  present: number;
  absent: number;
  percentage: number;
  status: string;
}

export function AttendanceScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [attendance, setAttendance] = useState<Attendance[]>([]);

  useEffect(() => {
    loadAttendance();
  }, []);

  const loadAttendance = async () => {
    try {
      const result = await studentApi.attendance();
      if (result.success) {
        const data = Array.isArray(result.data) ? result.data : result.data.results || [];
        setAttendance(data);
      }
    } catch (error) {
      console.error('Load attendance error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadAttendance();
  };

  const getStatusColor = (percentage: number) => {
    if (percentage >= 75) return '#22c55e';
    if (percentage >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getStatusText = (percentage: number) => {
    if (percentage >= 75) return 'Good';
    if (percentage >= 50) return 'Warning';
    return 'Critical';
  };

  // Calculate overall attendance
  const overallPercentage = attendance.length > 0
    ? Math.round(attendance.reduce((sum, a) => sum + a.percentage, 0) / attendance.length)
    : 0;

  const totalPresent = attendance.reduce((sum, a) => sum + a.present, 0);
  const totalAbsent = attendance.reduce((sum, a) => sum + a.absent, 0);

  const renderAttendance = ({ item }: { item: Attendance }) => (
    <View style={styles.attendanceCard}>
      <View style={styles.attendanceHeader}>
        <View>
          <Text style={styles.courseCode}>{item.course_code}</Text>
          <Text style={styles.courseName}>{item.course_name}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.percentage) + '20' }]}>
          <Text style={[styles.statusText, { color: getStatusColor(item.percentage) }]}>
            {getStatusText(item.percentage)}
          </Text>
        </View>
      </View>

      {/* Progress Bar */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              { width: `${item.percentage}%`, backgroundColor: getStatusColor(item.percentage) },
            ]}
          />
        </View>
        <Text style={[styles.percentageText, { color: getStatusColor(item.percentage) }]}>
          {item.percentage}%
        </Text>
      </View>

      {/* Stats */}
      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Ionicons name="checkmark-circle" size={16} color="#22c55e" />
          <Text style={styles.statText}>{item.present} Present</Text>
        </View>
        <View style={styles.statItem}>
          <Ionicons name="close-circle" size={16} color="#ef4444" />
          <Text style={styles.statText}>{item.absent} Absent</Text>
        </View>
        <View style={styles.statItem}>
          <Ionicons name="calendar" size={16} color="#666" />
          <Text style={styles.statText}>{item.total} Total</Text>
        </View>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading attendance...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Attendance</Text>
        
        {/* Overall Stats */}
        <View style={styles.overallCard}>
          <View style={styles.overallMain}>
            <Text style={styles.overallLabel}>Overall Attendance</Text>
            <Text style={[styles.overallValue, { color: getStatusColor(overallPercentage) }]}>
              {overallPercentage}%
            </Text>
          </View>
          <View style={styles.overallStats}>
            <View style={styles.overallStat}>
              <Text style={styles.overallStatValue}>{totalPresent}</Text>
              <Text style={styles.overallStatLabel}>Present</Text>
            </View>
            <View style={styles.overallStat}>
              <Text style={styles.overallStatValue}>{totalAbsent}</Text>
              <Text style={styles.overallStatLabel}>Absent</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Warning if below 75% */}
      {overallPercentage > 0 && overallPercentage < 75 && (
        <View style={styles.warningBanner}>
          <Ionicons name="warning" size={20} color="#f59e0b" />
          <Text style={styles.warningText}>
            Your attendance is below 75%. Attend more classes to avoid missing exams.
          </Text>
        </View>
      )}

      {/* Attendance List */}
      {attendance.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="finger-print-outline" size={60} color="#ccc" />
          <Text style={styles.emptyText}>No attendance records</Text>
          <Text style={styles.emptySubtext}>Attendance will appear after lectures begin</Text>
        </View>
      ) : (
        <FlatList
          data={attendance}
          renderItem={renderAttendance}
          keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
          contentContainerStyle={styles.listContainer}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
        />
      )}
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
    marginBottom: 15,
  },
  overallCard: {
    backgroundColor: 'rgba(255,255,255,0.15)',
    borderRadius: 12,
    padding: 15,
  },
  overallMain: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  overallLabel: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  overallValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  overallStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  overallStat: {
    alignItems: 'center',
  },
  overallStatValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  overallStatLabel: {
    fontSize: 12,
    color: '#fff',
    opacity: 0.8,
  },
  warningBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef3c7',
    padding: 12,
    margin: 15,
    borderRadius: 8,
  },
  warningText: {
    flex: 1,
    marginLeft: 10,
    fontSize: 13,
    color: '#92400e',
  },
  listContainer: {
    padding: 15,
  },
  attendanceCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  attendanceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  courseCode: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  courseName: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  progressBar: {
    flex: 1,
    height: 8,
    backgroundColor: '#e5e5e5',
    borderRadius: 4,
    marginRight: 10,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  percentageText: {
    fontSize: 16,
    fontWeight: 'bold',
    width: 45,
    textAlign: 'right',
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    marginTop: 15,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 5,
  },
});
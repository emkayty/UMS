/**
 * Transcript Screen
 * Academic transcript - API integrated
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
import { studentApi } from '../services/api';

interface Props {
  navigation: any;
}

export function TranscriptScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    loadTranscript();
  }, []);

  const loadTranscript = async () => {
    try {
      const profileRes = await studentApi.profile();
      if (profileRes.success) {
        setProfile(profileRes.data);
      }

      const resultsRes = await studentApi.results();
      if (resultsRes.success) {
        const data = Array.isArray(resultsRes.data) ? resultsRes.data : resultsRes.data.results || [];
        setResults(data);
      }
    } catch (error) {
      console.error('Load transcript error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading transcript...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Transcript</Text>
        <TouchableOpacity style={styles.printButton}>
          <Ionicons name="print-outline" size={20} color={COLORS.primary} />
          <Text style={styles.printButtonText}>Print</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* Student Info */}
        <View style={styles.infoCard}>
          <View style={styles.infoHeader}>
            <View style={styles.avatarPlaceholder}>
              <Text style={styles.avatarText}>
                {(profile?.first_name?.[0] || 'S')}{(profile?.last_name?.[0] || '')}
              </Text>
            </View>
            <View style={styles.infoDetails}>
              <Text style={styles.studentName}>
                {profile?.first_name} {profile?.last_name}
              </Text>
              <Text style={styles.studentMatric}>{profile?.matric_number}</Text>
              <Text style={styles.studentProgramme}>{profile?.programme}</Text>
            </View>
          </View>
        </View>

        {/* Academic Summary */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Academic Summary</Text>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Level</Text>
              <Text style={styles.summaryValue}>{profile?.current_level || '100'}</Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>CGPA</Text>
              <Text style={styles.summaryValue}>{profile?. cgpa || '0.0'}</Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Status</Text>
              <Text style={styles.summaryValue}>{profile?.status || 'Active'}</Text>
            </View>
          </View>
        </View>

        {/* Course Record */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Course Record</Text>
          {results.length === 0 ? (
            <Text style={styles.noData}>No courses on record</Text>
          ) : (
            results.slice(0, 10).map((result: any, index: number) => (
              <View key={index} style={styles.courseRow}>
                <View style={styles.courseInfo}>
                  <Text style={styles.courseCode}>{result.course_code}</Text>
                  <Text style={styles.courseName}>{result.course_name}</Text>
                </View>
                <View style={styles.courseGrade}>
                  <Text style={styles.gradeText}>{result.grade}</Text>
                </View>
              </View>
            ))
          )}
        </View>

        {/* Request Transcript */}
        <TouchableOpacity style={styles.requestButton}>
          <Ionicons name="document-text-outline" size={20} color="#fff" />
          <Text style={styles.requestButtonText}>Request Official Transcript</Text>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  printButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
  },
  printButtonText: {
    color: COLORS.primary,
    fontSize: 14,
    marginLeft: 5,
  },
  content: {
    flex: 1,
    padding: 15,
  },
  infoCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
  },
  infoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatarPlaceholder: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  infoDetails: {
    marginLeft: 15,
  },
  studentName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  studentMatric: {
    fontSize: 14,
    color: '#666',
  },
  studentProgramme: {
    fontSize: 13,
    color: '#666',
  },
  card: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 15,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 12,
    color: '#666',
  },
  summaryValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  noData: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
  },
  courseRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  courseInfo: {
    flex: 1,
  },
  courseCode: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  courseName: {
    fontSize: 12,
    color: '#666',
  },
  courseGrade: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 4,
  },
  gradeText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  requestButton: {
    backgroundColor: COLORS.primary,
    padding: 15,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  requestButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 10,
  },
});
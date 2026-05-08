/**
 * Admission Screen
 * Admission portal - API integrated
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
import { academicApi } from '../services/api';

interface Props {
  navigation: any;
}

export function AdmissionScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState<any>(null);
  const [programmes, setProgrammes] = useState<any[]>([]);

  useEffect(() => {
    loadAdmission();
  }, []);

  const loadAdmission = async () => {
    try {
      const sessionRes = await academicApi.session();
      if (sessionRes.success) {
        setSession(sessionRes.data);
      }

      const progRes = await academicApi.programmes();
      if (progRes.success) {
        const data = Array.isArray(progRes.data) ? progRes.data : progRes.data.results || [];
        setProgrammes(data);
      }
    } catch (error) {
      console.error('Load admission error:', error);
    } finally {
      setLoading(false);
    }
  };

  const admissionSteps = [
    { number: 1, title: 'Application', icon: 'create', status: 'completed' },
    { number: 2, title: 'Screening', icon: 'finger-print', status: 'pending' },
    { number: 3, title: 'Interview', icon: 'people', status: 'pending' },
    { number: 4, title: 'Admission', icon: 'school', status: 'pending' },
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
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Admission</Text>
        <Text style={styles.headerSubtitle}>
          {session?.name || '2024/2025'} Academic Session
        </Text>
      </View>

      <ScrollView style={styles.content}>
        {/* Current Status */}
        <View style={styles.statusCard}>
          <Text style={styles.statusTitle}>Application Status</Text>
          <View style={styles.statusRow}>
            <View style={[styles.statusBadge, { backgroundColor: '#d1fae5' }]}>
              <Text style={[styles.statusBadgeText, { color: '#065f46' }]}>
                Closed
              </Text>
            </View>
            <Text style={styles.statusNote}>
              Next session opens soon
            </Text>
          </View>
        </View>

        {/* Steps */}
        <Text style={styles.sectionTitle}>Admission Process</Text>
        {admissionSteps.map((step, index) => (
          <View key={index} style={styles.stepCard}>
            <View style={[styles.stepNumber, step.status === 'completed' && styles.stepNumberDone]}>
              {step.status === 'completed' ? (
                <Ionicons name="checkmark" size={16} color="#fff" />
              ) : (
                <Text style={styles.stepNumberText}>{step.number}</Text>
              )}
            </View>
            <View style={styles.stepInfo}>
              <Text style={styles.stepTitle}>{step.title}</Text>
              <Text style={styles.stepDescription}>
                {step.status === 'completed' ? 'Completed' : 'Pending'}
              </Text>
            </View>
            <Ionicons
              name={step.icon as any}
              size={20}
              color={step.status === 'completed' ? '#22c55e' : '#ccc'}
            />
          </View>
        ))}

        {/* Programmes */}
        <Text style={styles.sectionTitle}>Programmes</Text>
        <View style={styles.programmesCard}>
          {programmes.length === 0 ? (
            <Text style={styles.noData}>No programmes available</Text>
          ) : (
            programmes.slice(0, 5).map((prog: any, index: number) => (
              <View key={index} style={styles.programmeItem}>
                <Text style={styles.programmeName}>{prog.name}</Text>
                <Text style={styles.programmeCode}>{prog.code}</Text>
              </View>
            ))
          )}
        </View>

        {/* CTA */}
        <TouchableOpacity style={styles.applyButton}>
          <Ionicons name="create-outline" size={20} color="#fff" />
          <Text style={styles.applyButtonText}>Apply Now</Text>
        </TouchableOpacity>

        <Text style={styles.helpText}>
          Need help? Contact: admissions@uni.edu.ng
        </Text>
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
  statusCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 20,
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  statusBadgeText: {
    fontSize: 14,
    fontWeight: '600',
  },
  statusNote: {
    fontSize: 14,
    color: '#666',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 15,
  },
  stepCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  stepNumber: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#e5e5e5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  stepNumberDone: {
    backgroundColor: '#22c55e',
  },
  stepNumberText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#666',
  },
  stepInfo: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  stepDescription: {
    fontSize: 13,
    color: '#666',
  },
  programmesCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 20,
  },
  programmeItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  programmeName: {
    fontSize: 14,
    color: '#333',
  },
  programmeCode: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '600',
  },
  noData: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    textAlign: 'center',
  },
  applyButton: {
    backgroundColor: COLORS.primary,
    padding: 15,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  applyButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 10,
  },
  helpText: {
    textAlign: 'center',
    fontSize: 13,
    color: '#666',
    marginBottom: 30,
  },
});
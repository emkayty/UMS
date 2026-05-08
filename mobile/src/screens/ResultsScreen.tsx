/**
 * Results Screen
 * Student academic results - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
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

interface Result {
  id: number;
  course_code: string;
  course_name: string;
  score: number;
  grade: string;
  grade_point: number;
  semester: string;
  session: string;
}

export function ResultsScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [results, setResults] = useState<Result[]>([]);
  const [cgpa, setCgpa] = useState('0.0');
  const [selectedSession, setSelectedSession] = useState('all');

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      const result = await studentApi.results();
      if (result.success) {
        const data = Array.isArray(result.data) ? result.data : result.data.results || [];
        setResults(data);
        
        // Calculate CGPA from results
        if (data.length > 0) {
          const totalPoints = data.reduce((sum: number, r: Result) => sum + (r.grade_point || 0), 0);
          const avg = totalPoints / data.length;
          setCgpa(avg.toFixed(2));
        }
      }
    } catch (error) {
      console.error('Load results error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadResults();
  };

  const getGradeColor = (grade: string) => {
    const g = grade?.toUpperCase();
    if (g === 'A' || g === 'A+') return '#22c55e';
    if (g === 'B') return '#3b82f6';
    if (g === 'C') return '#f59e0b';
    if (g === 'D') return '#f97316';
    return '#ef4444';
  };

  const getGradePoint = (gp: number) => {
    if (gp >= 4.0) return 'Excellent';
    if (gp >= 3.5) return 'Very Good';
    if (gp >= 3.0) return 'Good';
    if (gp >= 2.0) return 'Pass';
    return 'Fail';
  };

  const renderResult = ({ item }: { item: Result }) => (
    <View style={styles.resultCard}>
      <View style={styles.resultHeader}>
        <View>
          <Text style={styles.courseCode}>{item.course_code}</Text>
          <Text style={styles.courseName}>{item.course_name}</Text>
        </View>
        <View style={[styles.gradeCircle, { backgroundColor: getGradeColor(item.grade) + '20' }]}>
          <Text style={[styles.gradeText, { color: getGradeColor(item.grade) }]}>
            {item.grade}
          </Text>
        </View>
      </View>
      <View style={styles.resultDetails}>
        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Score</Text>
          <Text style={styles.detailValue}>{item.score}</Text>
        </View>
        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Point</Text>
          <Text style={styles.detailValue}>{item.grade_point?.toFixed(1)}</Text>
        </View>
        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Semester</Text>
          <Text style={styles.detailValue}>{item.semester}</Text>
        </View>
      </View>
      <Text style={styles.gradeRemark}>{getGradePoint(item.grade_point)}</Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading results...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Academic Results</Text>
        <View style={styles.cgpaCard}>
          <Text style={styles.cgpaLabel}>CGPA</Text>
          <Text style={styles.cgpaValue}>{cgpa}</Text>
        </View>
      </View>

      {/* Summary */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>{results.length}</Text>
          <Text style={styles.summaryLabel}>Courses</Text>
        </View>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {results.filter((r: Result) => r.grade?.startsWith('A')).length}
          </Text>
          <Text style={styles.summaryLabel}>A's</Text>
        </View>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {results.filter((r: Result) => r.score < 40).length}
          </Text>
          <Text style={styles.summaryLabel}>Failed</Text>
        </View>
      </View>

      {/* Results List */}
      {results.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="school-outline" size={60} color="#ccc" />
          <Text style={styles.emptyText}>No results available</Text>
          <Text style={styles.emptySubtext}>Results will appear after semester ends</Text>
        </View>
      ) : (
        <FlatList
          data={results}
          renderItem={renderResult}
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  cgpaCard: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 10,
    borderRadius: 10,
    alignItems: 'center',
  },
  cgpaLabel: {
    fontSize: 12,
    color: '#fff',
    opacity: 0.8,
  },
  cgpaValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  summaryContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 12,
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  summaryLabel: {
    fontSize: 12,
    color: '#666',
  },
  listContainer: {
    padding: 15,
  },
  resultCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  courseCode: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  courseName: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  gradeCircle: {
    width: 45,
    height: 45,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  gradeText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  resultDetails: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  detailItem: {
    flex: 1,
  },
  detailLabel: {
    fontSize: 11,
    color: '#999',
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  gradeRemark: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
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
/**
 * Courses Screen
 * Student registered courses - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { studentApi } from '../services/api';

interface Props {
  navigation: any;
}

interface Course {
  id: number;
  code: string;
  name: string;
  credits: number;
  semester: string;
  status: string;
}

export function CoursesScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedSemester, setSelectedSemester] = useState('all');

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const result = await studentApi.courses();
      if (result.success) {
        // Handle both array and object responses
        const data = Array.isArray(result.data) ? result.data : result.data.results || [];
        setCourses(data);
      }
    } catch (error) {
      console.error('Load courses error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadCourses();
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'registered': return '#22c55e';
      case 'completed': return '#3b82f6';
      case 'failed': return '#ef4444';
      default: return '#f59e0b';
    }
  };

  const renderCourse = ({ item }: { item: Course }) => (
    <View style={styles.courseCard}>
      <View style={styles.courseHeader}>
        <Text style={styles.courseCode}>{item.code}</Text>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) + '20' }]}>
          <Text style={[styles.statusText, { color: getStatusColor(item.status) }]}>
            {item.status || 'Registered'}
          </Text>
        </View>
      </View>
      <Text style={styles.courseName}>{item.name}</Text>
      <View style={styles.courseFooter}>
        <View style={styles.courseInfo}>
          <Ionicons name="time-outline" size={14} color="#666" />
          <Text style={styles.courseInfoText}>{item.credits} Credits</Text>
        </View>
        <View style={styles.courseInfo}>
          <Ionicons name="calendar-outline" size={14} color="#666" />
          <Text style={styles.courseInfoText}>{item.semester || 'First Semester'}</Text>
        </View>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading courses...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Courses</Text>
        <Text style={styles.headerSubtitle}>
          {courses.length} Course{courses.length !== 1 ? 's' : ''} Registered
        </Text>
      </View>

      {/* Filter */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterContainer}>
        <TouchableOpacity
          style={[styles.filterChip, selectedSemester === 'all' && styles.filterChipActive]}
          onPress={() => setSelectedSemester('all')}
        >
          <Text style={[styles.filterText, selectedSemester === 'all' && styles.filterTextActive]}>
            All
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterChip, selectedSemester === 'first' && styles.filterChipActive]}
          onPress={() => setSelectedSemester('first')}
        >
          <Text style={[styles.filterText, selectedSemester === 'first' && styles.filterTextActive]}>
            First Semester
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterChip, selectedSemester === 'second' && styles.filterChipActive]}
          onPress={() => setSelectedSemester('second')}
        >
          <Text style={[styles.filterText, selectedSemester === 'second' && styles.filterTextActive]}>
            Second Semester
          </Text>
        </TouchableOpacity>
      </ScrollView>

      {/* Course List */}
      {courses.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="book-outline" size={60} color="#ccc" />
          <Text style={styles.emptyText}>No courses registered</Text>
          <Text style={styles.emptySubtext}>
            Course registration is currently closed
          </Text>
        </View>
      ) : (
        <FlatList
          data={courses}
          renderItem={renderCourse}
          keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
          contentContainerStyle={styles.listContainer}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
        />
      )}

      {/* Add Course Button */}
      <TouchableOpacity style={styles.addButton}>
        <Ionicons name="add" size={24} color="#fff" />
      </TouchableOpacity>
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
    marginTop: 4,
  },
  filterContainer: {
    backgroundColor: '#fff',
    padding: 10,
  },
  filterChip: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    marginRight: 10,
  },
  filterChipActive: {
    backgroundColor: COLORS.primary,
  },
  filterText: {
    fontSize: 14,
    color: '#666',
  },
  filterTextActive: {
    color: '#fff',
  },
  listContainer: {
    padding: 15,
  },
  courseCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  courseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  courseCode: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.primary,
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
  courseName: {
    fontSize: 14,
    color: '#333',
    marginBottom: 10,
  },
  courseFooter: {
    flexDirection: 'row',
  },
  courseInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 20,
  },
  courseInfoText: {
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
  addButton: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
});
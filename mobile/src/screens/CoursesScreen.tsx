/**
 * UMS Mobile - Courses Screen
 * Course listing and enrollment
 */

import React, { useState } from 'react';
import { View, Text, TextInput, FlatList, TouchableOpacity, StyleSheet, RefreshControl } from 'react-native';
import { COLORS } from '../config';

interface Course {
  id: string;
  code: string;
  title: string;
  credits: number;
  lecturer: string;
  semester: string;
  enrolled: number;
  maxCapacity: number;
  status: 'open' | 'closed' | 'pending';
}

const mockCourses: Course[] = [
  { id: '1', code: 'CS101', title: 'Introduction to Computer Science', credits: 3, lecturer: 'Dr. Smith', semester: 'First', enrolled: 45, maxCapacity: 50, status: 'open' },
  { id: '2', code: 'CS201', title: 'Data Structures', credits: 4, lecturer: 'Prof. Johnson', semester: 'First', enrolled: 30, maxCapacity: 40, status: 'open' },
  { id: '3', code: 'MATH101', title: 'Calculus I', credits: 3, lecturer: 'Dr. Williams', semester: 'First', enrolled: 60, maxCapacity: 60, status: 'closed' },
  { id: '4', code: 'ENG101', title: 'English Communication', credits: 2, lecturer: 'Ms. Brown', semester: 'First', enrolled: 35, maxCapacity: 40, status: 'open' },
  { id: '5', code: 'PHY101', title: 'Physics I', credits: 3, lecturer: 'Prof. Davis', semester: 'First', enrolled: 40, maxCapacity: 45, status: 'open' },
];

export default function CoursesScreen() {
  const [courses, setCourses] = useState<Course[]>(mockCourses);
  const [search, setSearch] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1000);
  };

  const filteredCourses = courses.filter(c => 
    c.title.toLowerCase().includes(search.toLowerCase()) ||
    c.code.toLowerCase().includes(search.toLowerCase())
  );

  const renderCourse = ({ item }: { item: Course }) => (
    <TouchableOpacity style={styles.courseCard}>
      <View style={styles.courseHeader}>
        <Text style={styles.courseCode}>{item.code}</Text>
        <View style={[styles.status, item.status === 'open' ? styles.open : styles.closed]}>
          <Text style={styles.statusText}>{item.status.toUpperCase()}</Text>
        </View>
      </View>
      <Text style={styles.courseTitle}>{item.title}</Text>
      <View style={styles.courseInfo}>
        <Text style={styles.infoText}>{item.credits} Credits</Text>
        <Text style={styles.infoText}>•</Text>
        <Text style={styles.infoText}>{item.lecturer}</Text>
      </View>
      <View style={styles.courseFooter}>
        <Text style={styles.enrolled}>{item.enrolled}/{item.maxCapacity} enrolled</Text>
        <TouchableOpacity 
          style={[styles.enrollButton, item.status === 'closed' && styles.buttonDisabled]}
          disabled={item.status === 'closed'}
        >
          <Text style={styles.enrollText}>
            {item.status === 'open' ? 'Enroll' : 'Closed'}
          </Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Courses</Text>
        <Text style={styles.subtitle}>{courses.length} courses available</Text>
      </View>
      
      <View style={styles.search}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search courses..."
          value={search}
          onChangeText={setSearch}
        />
      </View>
      
      <FlatList
        data={filteredCourses}
        renderItem={renderCourse}
        keyExtractor={item => item.id}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />
        }
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.gray[50],
  },
  header: {
    padding: 20,
    backgroundColor: COLORS.primary,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.white,
    opacity: 0.8,
    marginTop: 4,
  },
  search: {
    padding: 15,
    backgroundColor: COLORS.white,
  },
  searchInput: {
    padding: 12,
    borderRadius: 10,
    backgroundColor: COLORS.gray[50],
  },
  list: {
    padding: 15,
  },
  courseCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: 15,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
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
  status: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  open: {
    backgroundColor: COLORS.success + '20',
  },
  closed: {
    backgroundColor: COLORS.error + '20',
  },
  statusText: {
    fontSize: 10,
    fontWeight: '600',
  },
  courseTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.gray[800],
    marginBottom: 8,
  },
  courseInfo: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  infoText: {
    fontSize: 12,
    color: COLORS.gray[600],
  },
  courseFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: 12,
  },
  enrolled: {
    fontSize: 12,
    color: COLORS.gray[600],
  },
  enrollButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: COLORS.primary,
    borderRadius: 6,
  },
  buttonDisabled: {
    backgroundColor: COLORS.gray[300],
  },
  enrollText: {
    color: COLORS.white,
    fontWeight: '600',
    fontSize: 12,
  },
});
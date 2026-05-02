import React from 'react'
import { View, Text, StyleSheet, FlatList } from 'react-native'

export function ResultsScreen() {
  const semesters = [
    { name: 'First Semester 2023/2024', gpa: 3.85, courses: 5 },
    { name: 'Second Semester 2023/2024', gpa: 3.65, courses: 5 },
    { name: 'First Semester 2024/2025', gpa: 3.75, courses: 5 },
  ]

  return (
    <View style={styles.container}>
      <View style={styles.cgpaCard}>
        <Text style={styles.cgpaLabel}>Current CGPA</Text>
        <Text style={styles.cgpaValue}>3.75</Text>
      </View>

      <FlatList
        data={semesters}
        keyExtractor={(item) => item.name}
        renderItem={({ item }) => (
          <View style={styles.semesterCard}>
            <Text style={styles.semesterName}>{item.name}</Text>
            <View style={styles.semesterStats}>
              <Text style={styles.gpa}>GPA: {item.gpa}</Text>
              <Text style={styles.courses}>Courses: {item.courses}</Text>
            </View>
          </View>
        )}
      />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f9fafb', padding: 16 },
  cgpaCard: { backgroundColor: '#22c55e', borderRadius: 16, padding: 24, alignItems: 'center', marginBottom: 16 },
  cgpaLabel: { color: 'white', fontSize: 14 },
  cgpaValue: { color: 'white', fontSize: 48, fontWeight: 'bold' },
  semesterCard: { backgroundColor: 'white', borderRadius: 12, padding: 16, marginBottom: 12 },
  semesterName: { fontSize: 16, fontWeight: '600', color: '#1f2937' },
  semesterStats: { flexDirection: 'row', marginTop: 8, gap: 16 },
  gpa: { color: '#22c55e', fontWeight: '600' },
  courses: { color: '#6b7280' },
})

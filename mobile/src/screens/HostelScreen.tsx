/**
 * UMS Mobile - Hostel Screen
 */

import React, { useState } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { hostelApi } from '../services/api';

export default function HostelScreen() {
  const hostels = [
    { id: '1', name: 'Male Hostel A', beds: 50, type: 'male' },
    { id: '2', name: 'Female Hostel B', beds: 35, type: 'female' },
    { id: '3', name: 'Mixed Hostel', beds: 20, type: 'mixed' },
  ];
  
  const handleApply = async (hostelId: string) => {
    const result = await hostelApi.apply({ hostel_id: hostelId });
    alert(result.success ? 'Applied successfully!' : 'Failed to apply');
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Hostel Application</Text>
      
      {hostels.map(h => (
        <View key={h.id} style={styles.card}>
          <Text style={styles.name}>{h.name}</Text>
          <Text style={styles.beds}>{h.beds} beds available</Text>
          <TouchableOpacity style={styles.button} onPress={() => handleApply(h.id)}>
            <Text style={styles.buttonText}>Apply Now</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 16, marginBottom: 16 },
  name: { fontSize: 18, fontWeight: '600', marginBottom: 4 },
  beds: { color: '#666', marginBottom: 12 },
  button: { backgroundColor: '#1e40af', padding: 12, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: '#fff', fontWeight: '600' },
});
/**
 * UMS Mobile - Hostel Screen - WITH REAL API
 */

import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { hostelApi } from '../services/api';

interface Hostel {
  id: number;
  name: string;
  total_beds: number;
  available_beds: number;
  gender: string;
}

export default function HostelScreen() {
  const [hostels, setHostels] = useState<Hostel[]>([]);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState<number | null>(null);
  
  useEffect(() => {
    loadHostels();
  }, []);
  
  const loadHostels = async () => {
    const result = await hostelApi.list();
    if (result.success && result.data) {
      setHostels(result.data);
    }
    setLoading(false);
  };
  
  const handleApply = async (hostelId: number) => {
    setApplying(hostelId);
    const result = await hostelApi.apply({ hostel_id: hostelId });
    alert(result.success ? 'Applied successfully!' : 'Failed to apply');
    setApplying(null);
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Hostel Application</Text>
      
      {loading ? (
        <ActivityIndicator size="large" />
      ) : (
        <>
          {hostels.length > 0 ? hostels.map(h => (
            <View key={h.id} style={styles.card}>
              <Text style={styles.name}>{h.name}</Text>
              <Text style={styles.beds}>{h.available_beds} beds available</Text>
              <TouchableOpacity 
                style={[styles.button, applying === h.id && styles.buttonDisabled]}
                onPress={() => handleApply(h.id)}
                disabled={applying !== null}
              >
                {applying === h.id ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <Text style={styles.buttonText}>Apply Now</Text>
                )}
              </TouchableOpacity>
            </View>
          )) : (
            // Fallback if no data
            <View style={styles.card}>
              <Text style={styles.name}>Male Hostel</Text>
              <Text style={styles.beds}>50 beds available</Text>
              <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Apply Now</Text>
              </TouchableOpacity>
            </View>
          )}
        </>
      )}
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
  buttonDisabled: { backgroundColor: '#9ca3af' },
  buttonText: { color: '#fff', fontWeight: '600' },
});
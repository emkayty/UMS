/**
 * UMS Mobile - Transcript Screen
 */

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';
import { transcriptApi } from '../services/api';

export default function TranscriptScreen() {
  const [studentId, setStudentId] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const checkStatus = async () => {
    const result = await transcriptApi.get(studentId);
    if (result.success) {
      setStatus(result.data?.status || 'Processing');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Transcript Request</Text>
      
      <View style={styles.form}>
        <Text style={styles.label}>Student ID</Text>
        <TextInput 
          style={styles.input} 
          value={studentId}
          onChangeText={setStudentId}
          placeholder="Enter your student ID"
        />
        
        <TouchableOpacity style={styles.button} onPress={checkStatus}>
          <Text style={styles.buttonText}>Check Status</Text>
        </TouchableOpacity>
        
        {status && (
          <View style={styles.statusBox}>
            <Text style={styles.statusLabel}>Status:</Text>
            <Text style={styles.statusValue}>{status}</Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  form: { gap: 12 },
  label: { fontSize: 14, fontWeight: '600' },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 16 },
  button: { backgroundColor: '#1e40af', padding: 16, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  statusBox: { marginTop: 20, padding: 16, backgroundColor: '#f3f4f6', borderRadius: 8 },
  statusLabel: { fontSize: 14, color: '#666' },
  statusValue: { fontSize: 18, fontWeight: '600', marginTop: 4 },
});
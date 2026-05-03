/**
 * UMS Mobile - Admission Screen
 */

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';
import { admissionApi } from '../services/api';

export default function AdmissionScreen() {
  const [form, setForm] = useState({
    firstName: '', lastName: '', email: '',
    phone: '', program: 'nd', department: '',
  });

  const handleSubmit = async () => {
    const result = await admissionApi.submit(form);
    alert(result.success ? 'Application submitted!' : 'Failed');
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Admission Application</Text>
      
      <View style={styles.form}>
        <Text style={styles.label}>First Name</Text>
        <TextInput 
          style={styles.input} 
          value={form.firstName}
          onChangeText={(v) => setForm({...form, firstName: v})}
        />
        
        <Text style={styles.label}>Last Name</Text>
        <TextInput 
          style={styles.input} 
          value={form.lastName}
          onChangeText={(v) => setForm({...form, lastName: v})}
        />
        
        <Text style={styles.label}>Email</Text>
        <TextInput 
          style={styles.input} 
          value={form.email}
          onChangeText={(v) => setForm({...form, email: v})}
          keyboardType="email-address"
        />
        
        <Text style={styles.label}>Phone</Text>
        <TextInput 
          style={styles.input} 
          value={form.phone}
          onChangeText={(v) => setForm({...form, phone: v})}
          keyboardType="phone-pad"
        />
        
        <Text style={styles.label}>Program</Text>
        <View style={styles.options}>
          {['ND', 'HND', 'BSC'].map(p => (
            <TouchableOpacity 
              key={p}
              style={[styles.option, form.program === p && styles.optionSelected]}
              onPress={() => setForm({...form, program: p})}
            >
              <Text style={styles.optionText}>{p}</Text>
            </TouchableOpacity>
          ))}
        </View>
        
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Submit Application</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  form: { gap: 12 },
  label: { fontSize: 14, fontWeight: '600', marginBottom: 4 },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 16 },
  options: { flexDirection: 'row', gap: 8 },
  option: { padding: 12, borderRadius: 8, borderWidth: 1, borderColor: '#ddd' },
  optionSelected: { backgroundColor: '#1e40af', borderColor: '#1e40af' },
  optionText: { color: '#333' },
  button: { backgroundColor: '#1e40af', padding: 16, borderRadius: 8, marginTop: 20 },
  buttonText: { color: '#fff', textAlign: 'center', fontSize: 16, fontWeight: '600' },
});
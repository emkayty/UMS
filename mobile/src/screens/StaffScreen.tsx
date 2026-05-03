/**
 * UMS Mobile - Staff Screen
 * Staff directory and contact
 */

import React, { useState } from 'react';
import { View, Text, TextInput, FlatList, TouchableOpacity, StyleSheet, Image, Linking } from 'react-native';
import { COLORS } from '../config';

interface Staff {
  id: string;
  name: string;
  title: string;
  department: string;
  email: string;
  phone: string;
  photo?: string;
}

const mockStaff: Staff[] = [
  { id: '1', name: 'Prof. John Smith', title: 'Vice Chancellor', department: 'Administration', email: 'vc@unis versity.edu', phone: '+2348012345678' },
  { id: '2', name: 'Dr. Sarah Johnson', title: 'Dean, Faculty of Science', department: 'Science', email: 'sarah.j@university.edu', phone: '+2348012345679' },
  { id: '3', name: 'Prof. Michael Brown', title: 'Head of Computer Science', department: 'Computer Science', email: 'mbrown@university.edu', phone: '+2348012345680' },
  { id: '4', name: 'Dr. Emily Davis', title: 'Registrar', department: 'Registry', email: 'eregistrar@university.edu', phone: '+2348012345681' },
  { id: '5', name: 'Mr. David Wilson', title: 'Bursar', department: 'Finance', email: 'bursar@university.edu', phone: '+2348012345682' },
  { id: '6', name: 'Mrs. Jennifer Lee', title: 'Librarian', department: 'Library', email: 'library@university.edu', phone: '+2348012345683' },
];

export default function StaffScreen() {
  const [staff, setStaff] = useState<Staff[]>(mockStaff);
  const [search, setSearch] = useState('');
  const [selectedDept, setSelectedDept] = useState<string | null>(null);

  const departments = [...new Set(staff.map(s => s.department))];

  const filteredStaff = staff.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.title.toLowerCase().includes(search.toLowerCase());
    const matchesDept = !selectedDept || s.department === selectedDept;
    return matchesSearch && matchesDept;
  });

  const handleCall = (phone: string) => {
    Linking.openURL(`tel:${phone}`);
  };

  const handleEmail = (email: string) => {
    Linking.openURL(`mailto:${email}`);
  };

  const renderStaff = ({ item }: { item: Staff }) => (
    <View style={styles.staffCard}>
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>{item.name.charAt(0)}</Text>
      </View>
      <View style={styles.info}>
        <Text style={styles.name}>{item.name}</Text>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.department}>{item.department}</Text>
        <View style={styles.actions}>
          <TouchableOpacity style={styles.actionButton} onPress={() => handleCall(item.phone)}>
            <Text style={styles.actionText}>📞 Call</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionButton} onPress={() => handleEmail(item.email)}>
            <Text style={styles.actionText}>✉️ Email</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Staff Directory</Text>
        <Text style={styles.subtitle}>{staff.length} staff members</Text>
      </View>
      
      <View style={styles.search}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search staff..."
          value={search}
          onChangeText={setSearch}
        />
      </View>
      
      <View style={styles.filters}>
        <FlatList
          horizontal
          data={departments}
          keyExtractor={item => item}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={[styles.filter, selectedDept === item && styles.filterActive]}
              onPress={() => setSelectedDept(selectedDept === item ? null : item)}
            >
              <Text style={[styles.filterText, selectedDept === item && styles.filterTextActive]}>
                {item}
              </Text>
            </TouchableOpacity>
          )}
        />
      </View>
      
      <FlatList
        data={filteredStaff}
        renderItem={renderStaff}
        keyExtractor={item => item.id}
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
  filters: {
    paddingHorizontal: 15,
    paddingBottom: 10,
  },
  filter: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  filterText: {
    fontSize: 12,
    color: COLORS.gray[600],
  },
  filterTextActive: {
    color: COLORS.white,
  },
  list: {
    padding: 15,
  },
  staffCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: 15,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  info: {
    flex: 1,
    marginLeft: 12,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray[800],
  },
  title: {
    fontSize: 13,
    color: COLORS.gray[600],
    marginTop: 2,
  },
  department: {
    fontSize: 12,
    color: COLORS.primary,
    marginTop: 4,
  },
  actions: {
    flexDirection: 'row',
    marginTop: 10,
    gap: 10,
  },
  actionButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.gray[50],
    borderRadius: 6,
  },
  actionText: {
    fontSize: 12,
    color: COLORS.gray[700],
  },
});
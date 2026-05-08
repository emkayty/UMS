/**
 * Library Screen
 * Library services - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { learningApi } from '../services/api';

interface Props {
  navigation: any;
}

interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  available: boolean;
}

export function LibraryScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [materials, setMaterials] = useState<any[]>([]);
  const [borrowed, setBorrowed] = useState<any[]>([]);
  const [selectedTab, setSelectedTab] = useState('books');

  useEffect(() => {
    loadLibrary();
  }, []);

  const loadLibrary = async () => {
    try {
      const result = await learningApi.materials();
      if (result.success) {
        const data = Array.isArray(result.data) ? result.data : result.data.results || [];
        setMaterials(data);
      }
    } catch (error) {
      console.error('Load library error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadLibrary();
  };

  const filteredBooks = materials.filter((b: Book) =>
    b.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.author?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderBook = ({ item }: { item: Book }) => (
    <View style={styles.bookCard}>
      <View style={styles.bookInfo}>
        <Text style={styles.bookTitle}>{item.title}</Text>
        <Text style={styles.bookAuthor}>{item.author}</Text>
        <View style={styles.bookMeta}>
          <Ionicons name="bookmark-outline" size={14} color="#666" />
          <Text style={styles.bookMetaText}>{item.isbn}</Text>
        </View>
      </View>
      <View style={[styles.availabilityBadge, { backgroundColor: item.available ? '#d1fae5' : '#fee2e2' }]}>
        <Text style={[styles.availabilityText, { color: item.available ? '#065f46' : '#991b1b' }]}>
          {item.available ? 'Available' : 'Not Available'}
        </Text>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading library...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Library</Text>
      </View>

      {/* Search */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search books..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        <Ionicons name="search" size={20} color="#666" style={styles.searchIcon} />
      </View>

      {/* Tabs */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'books' && styles.tabActive]}
          onPress={() => setSelectedTab('books')}
        >
          <Text style={[styles.tabText, selectedTab === 'books' && styles.tabTextActive]}>
            Books
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'borrowed' && styles.tabActive]}
          onPress={() => setSelectedTab('borrowed')}
        >
          <Text style={[styles.tabText, selectedTab === 'borrowed' && styles.tabTextActive]}>
            Borrowed ({borrowed.length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {selectedTab === 'books' ? (
        filteredBooks.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="book-outline" size={60} color="#ccc" />
            <Text style={styles.emptyText}>No books found</Text>
          </View>
        ) : (
          <FlatList
            data={filteredBooks}
            renderItem={renderBook}
            keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
            contentContainerStyle={styles.listContainer}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
          />
        )
      ) : (
        <View style={styles.emptyContainer}>
          <Ionicons name="bookmarks-outline" size={60} color="#ccc" />
          <Text style={styles.emptyText}>No borrowed books</Text>
        </View>
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
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  searchContainer: {
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
  },
  searchInput: {
    flex: 1,
    padding: 15,
    fontSize: 16,
  },
  searchIcon: {
    marginRight: 15,
  },
  tabContainer: {
    flexDirection: 'row',
    marginHorizontal: 15,
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 4,
  },
  tab: {
    flex: 1,
    padding: 12,
    alignItems: 'center',
  },
  tabActive: {
    backgroundColor: COLORS.primary,
    borderRadius: 8,
  },
  tabText: {
    fontSize: 14,
    color: '#666',
  },
  tabTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
  listContainer: {
    padding: 15,
  },
  bookCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  bookInfo: {
    flex: 1,
  },
  bookTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  bookAuthor: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  bookMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 5,
  },
  bookMetaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  availabilityBadge: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  availabilityText: {
    fontSize: 12,
    fontWeight: '600',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    marginTop: 15,
  },
});
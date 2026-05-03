/**
 * UMS Mobile - Library Screen
 * Library services and book search
 */

import React, { useState } from 'react';
import { View, Text, TextInput, FlatList, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { COLORS } from '../config';

interface Book {
  id: string;
  title: string;
  author: string;
  isbn: string;
  category: string;
  available: number;
  total: number;
}

const mockBooks: Book[] = [
  { id: '1', title: 'Introduction to Algorithms', author: 'Cormen et al.', isbn: '978-0262033848', category: 'Computer Science', available: 3, total: 5 },
  { id: '2', title: 'Clean Code', author: 'Robert Martin', isbn: '978-0132350884', category: 'Computer Science', available: 2, total: 4 },
  { id: '3', title: 'Calculus: Early Transcendentals', author: 'James Stewart', isbn: '978-1285741550', category: 'Mathematics', available: 5, total: 8 },
  { id: '4', title: 'Physics for Scientists', author: 'Serway', isbn: '978-1305079127', category: 'Physics', available: 4, total: 6 },
  { id: '5', title: 'Organic Chemistry', author: 'Paula Bruice', isbn: '978-0134042282', category: 'Chemistry', available: 1, total: 3 },
];

interface BorrowedBook {
  id: string;
  title: string;
  dueDate: string;
  status: 'active' | 'overdue';
}

const mockBorrowed: BorrowedBook[] = [
  { id: '1', title: 'Clean Code', dueDate: '2026-05-10', status: 'active' },
];

export default function LibraryScreen() {
  const [search, setSearch] = useState('');
  const [books, setBooks] = useState<Book[]>(mockBooks);
  const [borrowed, setBorrowed] = useState<BorrowedBook[]>(mockBorrowed);

  const filteredBooks = books.filter(b => 
    b.title.toLowerCase().includes(search.toLowerCase()) ||
    b.author.toLowerCase().includes(search.toLowerCase())
  );

  const renderBook = ({ item }: { item: Book }) => (
    <View style={styles.bookCard}>
      <View style={styles.bookInfo}>
        <Text style={styles.bookTitle}>{item.title}</Text>
        <Text style={styles.author}>{item.author}</Text>
        <Text style={styles.isbn}>{item.isbn}</Text>
        <View style={styles.bookMeta}>
          <Text style={styles.category}>{item.category}</Text>
          <Text style={[styles.available, item.available === 0 && styles.unavailable]}>
            {item.available > 0 ? `${item.available} available` : 'Unavailable'}
          </Text>
        </View>
      </View>
      <TouchableOpacity 
        style={[styles.borrowButton, item.available === 0 && styles.buttonDisabled]}
        disabled={item.available === 0}
      >
        <Text style={styles.borrowText}>Borrow</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Library</Text>
        <Text style={styles.subtitle}>Search & borrow books</Text>
      </View>

      <ScrollView>
        {/* My Borrowed Books */}
        {borrowed.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>My Borrowed Books</Text>
            {borrowed.map(book => (
              <View key={book.id} style={styles.borrowedCard}>
                <Text style={styles.borrowedTitle}>{book.title}</Text>
                <Text style={styles.dueDate}>Due: {book.dueDate}</Text>
                <View style={[styles.status, book.status === 'overdue' && styles.overdue]}>
                  <Text style={styles.statusText}>{book.status.toUpperCase()}</Text>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* Search */}
        <View style={styles.searchSection}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search books by title or author..."
            value={search}
            onChangeText={setSearch}
          />
        </View>

        {/* Book List */}
        <View style={styles.booksSection}>
          <Text style={styles.sectionTitle}>All Books ({books.length})</Text>
          <FlatList
            data={filteredBooks}
            renderItem={renderBook}
            keyExtractor={item => item.id}
            scrollEnabled={false}
          />
        </View>
      </ScrollView>
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
  section: {
    padding: 15,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray[800],
    marginBottom: 10,
  },
  borrowedCard: {
    backgroundColor: COLORS.white,
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary,
  },
  borrowedTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.gray[800],
  },
  dueDate: {
    fontSize: 13,
    color: COLORS.gray[600],
    marginTop: 4,
  },
  status: {
    alignSelf: 'flex-start',
    marginTop: 8,
    paddingHorizontal: 8,
    paddingVertical: 4,
    backgroundColor: COLORS.success + '20',
    borderRadius: 4,
  },
  overdue: {
    backgroundColor: COLORS.error + '20',
  },
  statusText: {
    fontSize: 10,
    fontWeight: '600',
    color: COLORS.success,
  },
  searchSection: {
    padding: 15,
    backgroundColor: COLORS.white,
  },
  searchInput: {
    padding: 12,
    borderRadius: 10,
    backgroundColor: COLORS.gray[50],
  },
  booksSection: {
    padding: 15,
  },
  bookCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  bookInfo: {
    flex: 1,
  },
  bookTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray[800],
  },
  author: {
    fontSize: 12,
    color: COLORS.gray[600],
    marginTop: 4,
  },
  isbn: {
    fontSize: 11,
    color: COLORS.gray[400],
    marginTop: 2,
  },
  bookMeta: {
    flexDirection: 'row',
    marginTop: 8,
    gap: 10,
  },
  category: {
    fontSize: 11,
    color: COLORS.primary,
  },
  available: {
    fontSize: 11,
    color: COLORS.success,
  },
  unavailable: {
    color: COLORS.error,
  },
  borrowButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: COLORS.primary,
    borderRadius: 6,
    alignSelf: 'center',
  },
  buttonDisabled: {
    backgroundColor: COLORS.gray[300],
  },
  borrowText: {
    color: COLORS.white,
    fontWeight: '600',
    fontSize: 12,
  },
});
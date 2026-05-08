/**
 * Finance Screen
 * Student fees and payments - API integrated
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { studentApi } from '../services/api';

interface Props {
  navigation: any;
}

interface Fee {
  id: number;
  name: string;
  amount: number;
  due_date: string;
  status: string;
}

interface Payment {
  id: number;
  amount: number;
  date: string;
  reference: string;
  status: string;
}

export function FinanceScreen({ navigation }: Props) {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [fees, setFees] = useState<Fee[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [selectedTab, setSelectedTab] = useState('fees');

  useEffect(() => {
    loadFinance();
  }, []);

  const loadFinance = async () => {
    try {
      // Load fees
      const feesResult = await studentApi.fees();
      if (feesResult.success) {
        const feesData = Array.isArray(feesResult.data) ? feesResult.data : feesResult.data.results || [];
        setFees(feesData);
      }

      // Load payments
      const paymentsResult = await studentApi.payments();
      if (paymentsResult.success) {
        const paymentsData = Array.isArray(paymentsResult.data) ? paymentsResult.data : paymentsResult.data.results || [];
        setPayments(paymentsData);
      }
    } catch (error) {
      console.error('Load finance error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadFinance();
  };

  // Calculate totals
  const totalFees = fees.reduce((sum, f) => sum + f.amount, 0);
  const paidFees = fees.filter(f => f.status === 'paid').reduce((sum, f) => sum + f.amount, 0);
  const pendingFees = fees.filter(f => f.status !== 'paid').reduce((sum, f) => sum + f.amount, 0);
  const totalPaid = payments.reduce((sum, p) => sum + p.amount, 0);

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'paid':
      case 'success': return '#22c55e';
      case 'pending': return '#f59e0b';
      case 'failed': return '#ef4444';
      default: return '#666';
    }
  };

  const renderFee = ({ item }: { item: Fee }) => (
    <View style={styles.itemCard}>
      <View style={styles.itemHeader}>
        <View>
          <Text style={styles.itemName}>{item.name}</Text>
          <Text style={styles.itemDate}>Due: {item.due_date || 'N/A'}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) + '20' }]}>
          <Text style={[styles.statusText, { color: getStatusColor(item.status) }]}>
            {item.status || 'Pending'}
          </Text>
        </View>
      </View>
      <View style={styles.itemFooter}>
        <Text style={styles.itemAmount}>
          ₦{item.amount?.toLocaleString() || '0'}
        </Text>
        {item.status !== 'paid' && (
          <TouchableOpacity style={styles.payButton}>
            <Text style={styles.payButtonText}>Pay Now</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );

  const renderPayment = ({ item }: { item: Payment }) => (
    <View style={styles.itemCard}>
      <View style={styles.itemHeader}>
        <View>
          <Text style={styles.itemName}>Payment</Text>
          <Text style={styles.itemDate}>Ref: {item.reference || item.id}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) + '20' }]}>
          <Text style={[styles.statusText, { color: getStatusColor(item.status) }]}>
            {item.status || 'Success'}
          </Text>
        </View>
      </View>
      <View style={styles.itemFooter}>
        <Text style={[styles.itemAmount, { color: '#22c55e' }]}>
          ₦{item.amount?.toLocaleString() || '0'}
        </Text>
        <Text style={styles.itemDate}>{item.date}</Text>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading finance...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Finance</Text>
        
        {/* Summary Card */}
        <View style={styles.summaryCard}>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Total Fees</Text>
              <Text style={styles.summaryValue}>₦{totalFees.toLocaleString()}</Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Paid</Text>
              <Text style={[styles.summaryValue, { color: '#22c55e' }]}>
                ₦{totalPaid.toLocaleString()}
              </Text>
            </View>
          </View>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Balance</Text>
              <Text style={[styles.summaryValue, { color: pendingFees > 0 ? '#ef4444' : '#22c55e' }]}>
                ₦{pendingFees.toLocaleString()}
              </Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Status</Text>
              <Text style={[styles.summaryValue, { color: pendingFees > 0 ? '#f59e0b' : '#22c55e' }]}>
                {pendingFees > 0 ? 'Outstanding' : 'Cleared'}
              </Text>
            </View>
          </View>
        </View>
      </View>

      {/* Tabs */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'fees' && styles.tabActive]}
          onPress={() => setSelectedTab('fees')}
        >
          <Text style={[styles.tabText, selectedTab === 'fees' && styles.tabTextActive]}>
            Fees ({fees.length})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'payments' && styles.tabActive]}
          onPress={() => setSelectedTab('payments')}
        >
          <Text style={[styles.tabText, selectedTab === 'payments' && styles.tabTextActive]}>
            Payments ({payments.length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {selectedTab === 'fees' ? (
        fees.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="wallet-outline" size={60} color="#ccc" />
            <Text style={styles.emptyText}>No fees</Text>
          </View>
        ) : (
          <FlatList
            data={fees}
            renderItem={renderFee}
            keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
            contentContainerStyle={styles.listContainer}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
          />
        )
      ) : (
        payments.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="receipt-outline" size={60} color="#ccc" />
            <Text style={styles.emptyText}>No payments</Text>
          </View>
        ) : (
          <FlatList
            data={payments}
            renderItem={renderPayment}
            keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
            contentContainerStyle={styles.listContainer}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
          />
        )
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
    marginBottom: 15,
  },
  summaryCard: {
    backgroundColor: 'rgba(255,255,255,0.15)',
    borderRadius: 12,
    padding: 15,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  summaryItem: {
    flex: 1,
  },
  summaryLabel: {
    fontSize: 12,
    color: '#fff',
    opacity: 0.8,
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 10,
    padding: 4,
  },
  tab: {
    flex: 1,
    padding: 12,
    alignItems: 'center',
    borderRadius: 8,
  },
  tabActive: {
    backgroundColor: COLORS.primary,
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
    paddingTop: 0,
  },
  itemCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  itemName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  itemDate: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
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
  itemFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  itemAmount: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  payButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  payButtonText: {
    color: '#fff',
    fontSize: 14,
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
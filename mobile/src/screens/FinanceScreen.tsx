/**
 * Finance Screen
 * View fees and make payments
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { financeApi } from '../services/api';

export function FinanceScreen() {
  const [loading, setLoading] = useState(true);
  const [invoices, setInvoices] = useState<any[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  
  const loadData = async () => {
    try {
      const response = await financeApi.invoices();
      if (response.success) {
        setInvoices(response.data || []);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };
  
  useEffect(() => {
    loadData();
  }, []);
  
  const formatCurrency = (amount: number) => {
    return `₦${amount.toLocaleString()}`;
  };
  
  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'paid':
        return COLORS.success;
      case 'partial':
        return COLORS.warning;
      default:
        return COLORS.error;
    }
  };
  
  if (loading) {
    return (
      <View style={styles.centered}>
        <Text>Loading...</Text>
      </View>
    );
  }
  
  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.title}>Finance</Text>
        <Text style={styles.subtitle}>Fees and Payments</Text>
      </View>
      
      {/* Summary Card */}
      <View style={styles.summaryCard}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryLabel}>Total Due</Text>
          <Text style={styles.summaryValue}>
            {formatCurrency(invoices.reduce((sum, inv) => sum + (inv.amount_due || 0), 0))}
          </Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.summaryItem}>
          <Text style={styles.summaryLabel}>Paid</Text>
          <Text style={[styles.summaryValue, { color: COLORS.success }]}>
            {formatCurrency(invoices.reduce((sum, inv) => sum + (inv.amount_paid || 0), 0))}
          </Text>
        </View>
      </View>
      
      {/* Invoices List */}
      <Text style={styles.sectionTitle}>Invoices</Text>
      
      {!invoices.length ? (
        <View style={styles.empty}>
          <Ionicons name="receipt-outline" size={48} color={COLORS.gray[300]} />
          <Text style={styles.emptyText}>No invoices found</Text>
        </View>
      ) : (
        invoices.map((invoice, index) => (
          <View key={index} style={styles.invoiceCard}>
            <View style={styles.invoiceHeader}>
              <View>
                <Text style={styles.invoiceName}>{invoice.name || 'Fee'}</Text>
                <Text style={styles.invoiceDate}>{invoice.session || '2024/2025'}</Text>
              </View>
              <View style={[
                styles.statusBadge,
                { backgroundColor: getStatusColor(invoice.status) + '20' }
              ]}>
                <Text style={[
                  styles.statusText,
                  { color: getStatusColor(invoice.status) }
                ]}>
                  {invoice.status?.toUpperCase() || 'PENDING'}
                </Text>
              </View>
            </View>
            
            <View style={styles.invoiceAmount}>
              <Text style={styles.amountLabel}>Amount Due</Text>
              <Text style={styles.amountValue}>{formatCurrency(invoice.amount_due || 0)}</Text>
            </View>
            
            <View style={styles.invoiceAmount}>
              <Text style={styles.amountLabel}>Amount Paid</Text>
              <Text style={[styles.amountValue, { color: COLORS.success }]}>
                {formatCurrency(invoice.amount_paid || 0)}
              </Text>
            </View>
            
            {invoice.status !== 'paid' && (
              <TouchableOpacity style={styles.payButton}>
                <Ionicons name="card" size={18} color={COLORS.white} />
                <Text style={styles.payButtonText}>Pay Now</Text>
              </TouchableOpacity>
            )}
          </View>
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.gray[50],
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 20,
    backgroundColor: COLORS.primary,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.white,
    opacity: 0.8,
  },
  summaryCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    margin: 15,
    padding: 20,
    borderRadius: 12,
    elevation: 2,
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 12,
    color: COLORS.gray[500],
    marginBottom: 5,
  },
  summaryValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.gray[900],
  },
  divider: {
    width: 1,
    backgroundColor: COLORS.gray[200],
    marginVertical: 5,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.gray[900],
    margin: 15,
  },
  empty: {
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    marginTop: 10,
    color: COLORS.gray[400],
  },
  invoiceCard: {
    backgroundColor: COLORS.white,
    marginHorizontal: 15,
    marginBottom: 15,
    padding: 15,
    borderRadius: 12,
    elevation: 2,
  },
  invoiceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  invoiceName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.gray[900],
  },
  invoiceDate: {
    fontSize: 12,
    color: COLORS.gray[500],
    marginTop: 2,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 10,
    fontWeight: '600',
  },
  invoiceAmount: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  amountLabel: {
    fontSize: 14,
    color: COLORS.gray[500],
  },
  amountValue: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.gray[900],
  },
  payButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    padding: 12,
    borderRadius: 8,
    marginTop: 10,
  },
  payButtonText: {
    color: COLORS.white,
    fontWeight: '600',
    marginLeft: 8,
  },
});
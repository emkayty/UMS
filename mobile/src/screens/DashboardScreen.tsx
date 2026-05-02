import React, { useEffect, useState } from 'react'
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Animated, Dimensions } from 'react-native'

const { width } = Dimensions.get('window')

interface Props { navigation: any }

export function DashboardScreen({ navigation }: Props) {
  const [fadeAnim] = useState(new Animated.Value(0))
  const [scaleAnim] = useState(new Animated.Value(0.9))
  
  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 600, useNativeDriver: true }),
      Animated.spring(scaleAnim, { toValue: 1, friction: 8, tension: 40, useNativeDriver: true }),
    ]).start()
  }, [])
  
  const stats = [
    { label: 'GPA', value: 3.75, color: '#22c55e', icon: '📊' },
    { label: 'Courses', value: 5, color: '#3b82f6', icon: '📚' },
    { label: 'Due', value: 2, color: '#f59e0b', icon: '📝' },
    { label: 'Msgs', value: 3, color: '#8b5cf6', icon: '💬' },
  ]

  const quickActions = [
    { label: 'Courses', icon: '📚', screen: 'Courses', color: '#3b82f6' },
    { label: 'Results', icon: '📊', screen: 'Results', color: '#22c55e' },
    { label: 'Attendance', icon: '📱', screen: 'Attendance', color: '#f59e0b' },
    { label: 'Finance', icon: '💰', screen: 'Finance', color: '#8b5cf6' },
    { label: 'Library', icon: '📖', screen: 'Library', color: '#ef4444' },
    { label: 'Clearance', icon: '🎓', screen: 'Clearance', color: '#06b6d4' },
  ]

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <Animated.View style={[styles.header, { opacity: fadeAnim, transform: [{ scale: scaleAnim }]}]}>
        <Text style={styles.greeting}>Welcome back! 👋</Text>
        <Text style={styles.role}>Student • Year 2</Text>
        <View style={styles.sessionBadge}>
          <Text style={styles.sessionText}>2024/2025 Session</Text>
        </View>
      </Animated.View>

      <Animated.View style={{ opacity: fadeAnim, marginTop: -8 }}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.statsScroll}>
          {stats.map((stat, index) => (
            <Animated.View 
              key={stat.label} 
              style={[
                styles.statCard, 
                { borderLeftColor: stat.color },
                { transform: [{ translateY: index * 10 }] }
              ]}
            >
              <Text style={styles.statValue}>{stat.value}</Text>
              <Text style={styles.statLabel}>{stat.label}</Text>
            </Animated.View>
          ))}
        </ScrollView>
      </Animated.View>

      <Text style={styles.sectionTitle}>Quick Actions</Text>
      <View style={styles.actionsGrid}>
        {quickActions.map((action, index) => (
          <TouchableOpacity
            key={action.label}
            style={[styles.actionCard, { backgroundColor: action.color + '10' }]}
            onPress={() => navigation.navigate(action.screen)}
            activeOpacity={0.7}
          >
            <View style={[styles.actionIconBg, { backgroundColor: action.color + '20' }]}>
              <Text style={styles.actionIcon}>{action.icon}</Text>
            </View>
            <Text style={[styles.actionLabel, { color: action.color }]}>{action.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.bottomSpacer} />
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  header: { backgroundColor: '#1e40af', padding: 24, paddingTop: 20, borderBottomLeftRadius: 32, borderBottomRightRadius: 32, marginBottom: 16 },
  greeting: { color: 'white', fontSize: 28, fontWeight: 'bold' },
  role: { color: '#bfdbfe', fontSize: 14, marginTop: 4 },
  sessionBadge: { alignSelf: 'flex-start', marginTop: 12, paddingHorizontal: 12, paddingVertical: 6, backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: 20 },
  sessionText: { color: 'white', fontSize: 12, fontWeight: '600' },
  statsScroll: { paddingHorizontal: 16, gap: 12 },
  statCard: { backgroundColor: 'white', borderRadius: 16, padding: 16, minWidth: width * 0.35, borderLeftWidth: 4, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 10, elevation: 2 },
  statValue: { fontSize: 28, fontWeight: 'bold', color: '#1f2937' },
  statLabel: { fontSize: 12, color: '#6b7280', marginTop: 4 },
  sectionTitle: { fontSize: 18, fontWeight: '700', color: '#1f2937', marginHorizontal: 16, marginTop: 20, marginBottom: 12 },
  actionsGrid: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 16, gap: 12 },
  actionCard: { borderRadius: 16, padding: 16, alignItems: 'center', width: '30%', aspectRatio: 1 },
  actionIconBg: { width: 44, height: 44, borderRadius: 22, alignItems: 'center', justifyContent: 'center', marginBottom: 8 },
  actionIcon: { fontSize: 20 },
  actionLabel: { fontSize: 12, fontWeight: '600', textAlign: 'center' },
  bottomSpacer: { height: 100 },
})

import React, { useState, useEffect } from 'react'
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native'
import { CameraView, useCameraPermissions } from 'expo-camera'

export function AttendanceScreen() {
  const [permission, requestPermission] = useCameraPermissions()
  const [scanning, setScanning] = useState(false)

  const handleScan = () => {
    setScanning(true)
    Alert.alert('Scanning', 'Point camera at QR code', [
      { text: 'Cancel', onPress: () => setScanning(false) }
    ])
  }

  if (!permission) {
    return <View style={styles.container}><Text>Loading...</Text></View>
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Camera permission required</Text>
        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      {scanning ? (
        <CameraView style={styles.camera} facing="back" />
      ) : (
        <>
          <Text style={styles.title}>Attendance Scanner</Text>
          <Text style={styles.subtitle}>Scan QR code from lecturer</Text>
          
          <TouchableOpacity style={styles.scanButton} onPress={handleScan}>
            <Text style={styles.scanButtonText}>📱 Scan QR Code</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f9fafb', alignItems: 'center', justifyContent: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#1f2937' },
  subtitle: { color: '#6b7280', marginTop: 8, marginBottom: 32 },
  message: { color: '#6b7280', textAlign: 'center', marginBottom: 16 },
  button: { backgroundColor: '#1e40af', padding: 16, borderRadius: 12 },
  buttonText: { color: 'white', fontWeight: '600' },
  scanButton: { backgroundColor: '#1e40af', padding: 20, borderRadius: 16, width: '80%', alignItems: 'center' },
  scanButtonText: { color: 'white', fontSize: 18, fontWeight: '600' },
  camera: { flex: 1, width: '100%' },
})

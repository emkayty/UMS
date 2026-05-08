/**
 * Login Screen
 * User authentication with API integration
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../config';
import { authApi } from '../services/api';
import { saveToken } from '../services/storage';

export function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Please enter email and password');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await authApi.login(email, password);

      if (result.success && result.data?.access) {
        await saveToken(result.data.access);
        navigation.replace('Dashboard');
      } else {
        setError(result.error || 'Invalid credentials');
      }
    } catch (err: any) {
      setError(err.message || 'Connection failed. Check your network.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.logoContainer}>
          <Ionicons name="school" size={80} color={COLORS.primary} />
          <Text style={styles.title}>UniCore</Text>
          <Text style={styles.subtitle}>University Management</Text>
        </View>

        <View style={styles.form}>
          <Text style={styles.error}>{error}</Text>

          <View style={styles.inputContainer}>
            <Ionicons name="mail-outline" size={20} color={COLORS.gray[500]} />
            <TextInput
              style={styles.input}
              placeholder="Email address"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoComplete="email"
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={20} color={COLORS.gray[500]} />
            <TextInput
              style={styles.input}
              placeholder="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoCapitalize="none"
            />
          </View>

          <TouchableOpacity style={styles.forgotButton}>
            <Text style={styles.forgotText}>Forgot Password?</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.loginButton}
            onPress={handleLogin}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color={COLORS.white} />
            ) : (
              <Text style={styles.loginText}>Login</Text>
            )}
          </TouchableOpacity>

          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Need help? Contact ICT Support
            </Text>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.white,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginTop: 10,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.gray[600],
    marginTop: 5,
  },
  form: {
    width: '100%',
  },
  error: {
    color: COLORS.error,
    textAlign: 'center',
    marginBottom: 15,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.gray[100],
    borderRadius: 10,
    paddingHorizontal: 15,
    marginBottom: 15,
  },
  input: {
    flex: 1,
    padding: 15,
    fontSize: 16,
    color: COLORS.gray[900],
  },
  forgotButton: {
    alignSelf: 'flex-end',
    marginBottom: 20,
  },
  forgotText: {
    color: COLORS.primary,
    fontSize: 14,
  },
  loginButton: {
    backgroundColor: COLORS.primary,
    padding: 18,
    borderRadius: 10,
    alignItems: 'center',
  },
  loginText: {
    color: COLORS.white,
    fontSize: 16,
    fontWeight: '600',
  },
  footer: {
    marginTop: 30,
    alignItems: 'center',
  },
  footerText: {
    color: COLORS.gray[500],
    fontSize: 14,
  },
});

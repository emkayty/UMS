/**
 * UMS Mobile - AI Assistant Screen
 * AI-powered academic assistant
 */

import React, { useState } from 'react';
import { View, Text, TextInput, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { COLORS } from '../config';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function AIScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    
    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I\'m your AI academic assistant. How can I help you today? I can assist with:\n\n• Course information\n• Grades and results\n• Attendance queries\n• Fee payments\n• Academic calendar\n• And more!',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setLoading(false);
    }, 1500);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>AI Assistant</Text>
      </View>
      
      <ScrollView style={styles.messages}>
        {messages.length === 0 ? (
          <View style={styles.empty}>
            <Text style={styles.emptyText}>
              👋 Hi! I'm your AI academic assistant.
            </Text>
            <Text style={styles.emptySubtext}>
              Ask me anything about your courses, grades, attendance, or any academic matter.
            </Text>
          </View>
        ) : (
          messages.map(msg => (
            <View key={msg.id} style={[
              styles.message,
              msg.role === 'user' ? styles.userMessage : styles.assistantMessage
            ]}>
              <Text style={styles.messageText}>{msg.content}</Text>
            </View>
          ))
        )}
      </ScrollView>
      
      <View style={styles.input}>
        <TextInput
          style={styles.inputField}
          placeholder="Ask me anything..."
          value={input}
          onChangeText={setInput}
          multiline
        />
        <TouchableOpacity 
          style={[styles.sendButton, !input && styles.sendDisabled]}
          onPress={handleSend}
          disabled={!input || loading}
        >
          <Text style={styles.sendText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.white,
  },
  header: {
    padding: 20,
    backgroundColor: COLORS.primary,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  messages: {
    flex: 1,
    padding: 15,
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.primary,
    textAlign: 'center',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: COLORS.gray[600],
    textAlign: 'center',
  },
  message: {
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    maxWidth: '80%',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: COLORS.primary,
  },
  assistantMessage: {
    alignSelf: 'flex-start',
    backgroundColor: COLORS.gray[100],
  },
  messageText: {
    fontSize: 14,
    color: COLORS.gray[800],
  },
  input: {
    flexDirection: 'row',
    padding: 10,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  inputField: {
    flex: 1,
    padding: 12,
    borderRadius: 20,
    backgroundColor: COLORS.gray[50],
    marginRight: 10,
  },
  sendButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: COLORS.primary,
    borderRadius: 20,
  },
  sendDisabled: {
    opacity: 0.5,
  },
  sendText: {
    color: COLORS.white,
    fontWeight: '600',
  },
});
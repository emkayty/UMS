'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'

export default function AIAnalyticsPage() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<any>(null)
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([])
  const [chatInput, setChatInput] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<any[]>([])

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const res = await fetch('/api/v1/ai/ai/chat')
      const data = await res.json()
      setData(data)
    } catch (error) {
      console.error('Failed to fetch analytics')
    } finally {
      setLoading(false)
    }
  }

  const sendChat = async () => {
    if (!chatInput.trim()) return
    
    const userMsg = { role: 'user', content: chatInput }
    setChatMessages(prev => [...prev, userMsg])
    setChatInput('')

    try {
      const res = await fetch('/api/v1/ai/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: chatInput })
      })
      const data = await res.json()
      
      if (data.message) {
        setChatMessages(prev => [...prev, { role: 'assistant', content: data.message }])
      }
    } catch (error) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }])
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    try {
      const res = await fetch(`/api/v1/ai/ai/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await res.json()
      setSearchResults(data.results || [])
    } catch (error) {
      console.error('Search failed')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">AI & Analytics</h1>
        <p className="text-gray-600">Predictive analytics, risk assessment, and AI services</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="At-Risk Students" value="23" trend="+5" color="red" />
        <StatCard title="Avg Risk Score" value="12%" trend="-3%" color="green" />
        <StatCard title="AI Predictions" value="1,450" trend="+120" color="blue" />
        <StatCard title="Chat Sessions" value="89" trend="+15" color="purple" />
      </div>

      {/* Risk Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Risk Distribution</h2>
          <div className="space-y-3">
            <RiskBar label="Low Risk" count={850} percentage={68} color="green" />
            <RiskBar label="Medium Risk" count={280} percentage={22} color="yellow" />
            <RiskBar label="High Risk" count={85} percentage={7} color="orange" />
            <RiskBar label="Critical" count={35} percentage={3} color="red" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">AI Recommendations</h2>
          <div className="space-y-3">
            <RecommendationItem 
              title="Intervention Alert"
              description="15 students below 1.5 GPA - recommend counseling"
              type="warning"
            />
            <RecommendationItem 
              title="Enrollment Trend"
              description="Computer Science enrollment +15% predicted"
              type="success"
            />
            <RecommendationItem 
              title="Course Capacity"
              description="3 courses near capacity limit"
              type="info"
            />
          </div>
        </div>
      </div>

      {/* AI Chat & Search */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Chatbot */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold">AI Assistant</h2>
          </div>
          <div className="h-64 overflow-y-auto p-4 space-y-3">
            {chatMessages.length === 0 ? (
              <p className="text-gray-500 text-center">Ask me anything about the university!</p>
            ) : (
              chatMessages.map((msg, idx) => (
                <div key={idx} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'}`}>
                  <p className="text-sm">{msg.content}</p>
                </div>
              ))
            )}
          </div>
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 border rounded-md"
              />
              <button 
                onClick={sendChat}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Send
              </button>
            </div>
          </div>
        </div>

        {/* Smart Search */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold">Smart Search</h2>
          </div>
          <div className="p-4">
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search courses, policies..."
                className="flex-1 px-3 py-2 border rounded-md"
              />
              <button 
                onClick={handleSearch}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Search
              </button>
            </div>
            <div className="space-y-2">
              {searchResults.map((result, idx) => (
                <div key={idx} className="p-3 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer">
                  <p className="font-medium">{result.title}</p>
                  <p className="text-sm text-gray-500">Score: {result.score}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Predictive Models */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Active ML Models</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ModelCard name="Dropout Prediction" type="Random Forest" accuracy="87%" status="Production" />
          <ModelCard name="Grade Prediction" type="Gradient Boosting" accuracy="82%" status="Production" />
          <ModelCard name="Enrollment Forecast" type="Neural Network" accuracy="91%" status="Training" />
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, trend, color }: { title: string, value: string, trend: string, color: string }) {
  const colors: Record<string, string> = { red: 'text-red-600', green: 'text-green-600', blue: 'text-blue-600', purple: 'text-purple-600' }
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <p className="text-sm text-gray-500">{title}</p>
      <p className={`text-2xl font-bold ${colors[color]}`}>{value}</p>
      <p className={`text-xs ${trend.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>{trend} from last month</p>
    </div>
  )
}

function RiskBar({ label, count, percentage, color }: { label: string, count: number, percentage: number, color: string }) {
  const colors: Record<string, string> = { green: 'bg-green-500', yellow: 'bg-yellow-500', orange: 'bg-orange-500', red: 'bg-red-500' }
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span>{label}</span>
        <span>{count} ({percentage}%)</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div className={`h-2 rounded-full ${colors[color]}`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  )
}

function RecommendationItem({ title, description, type }: { title: string, description: string, type: string }) {
  const types: Record<string, string> = { warning: 'bg-yellow-50 border-yellow-200', success: 'bg-green-50 border-green-200', info: 'bg-blue-50 border-blue-200' }
  return (
    <div className={`p-3 rounded border ${types[type]}`}>
      <p className="font-medium text-sm">{title}</p>
      <p className="text-xs text-gray-600">{description}</p>
    </div>
  )
}

function ModelCard({ name, type, accuracy, status }: { name: string, type: string, accuracy: string, status: string }) {
  return (
    <div className="border rounded-lg p-4">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium">{name}</h3>
        <span className={`px-2 py-1 text-xs rounded ${status === 'Production' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
          {status}
        </span>
      </div>
      <p className="text-sm text-gray-500">{type}</p>
      <p className="mt-2 text-sm">Accuracy: {accuracy}</p>
    </div>
  )
}
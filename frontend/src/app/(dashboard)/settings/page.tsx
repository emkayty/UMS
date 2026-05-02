'use client'

import { useState } from 'react'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('branding')

  const tabs = [
    { id: 'branding', name: 'Branding' },
    { id: 'academic', name: 'Academic' },
    { id: 'grading', name: 'Grading' },
    { id: 'payments', name: 'Payments' },
    { id: 'notifications', name: 'Notifications' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      
      <div className="bg-white rounded-lg shadow">
        <div className="border-b">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'branding' && <BrandingSettings />}
          {activeTab === 'academic' && <AcademicSettings />}
          {activeTab === 'grading' && <GradingSettings />}
          {activeTab === 'payments' && <PaymentSettings />}
          {activeTab === 'notifications' && <NotificationSettings />}
        </div>
      </div>
    </div>
  )
}

function BrandingSettings() {
  const [settings, setSettings] = useState({
    name: 'University Name',
    motto: 'Education for Development',
    primaryColor: '#1e3a8a',
    secondaryColor: '#059669',
  })

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Institution Name</label>
        <input
          type="text"
          value={settings.name}
          onChange={(e) => setSettings({ ...settings, name: e.target.value })}
          className="mt-1 block w-full px-3 py-2 border rounded-md"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Motto</label>
        <input
          type="text"
          value={settings.motto}
          onChange={(e) => setSettings({ ...settings, motto: e.target.value })}
          className="mt-1 block w-full px-3 py-2 border rounded-md"
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Primary Color</label>
          <input type="color" value={settings.primaryColor} className="mt-1 h-10 w-full" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Secondary Color</label>
          <input type="color" value={settings.secondaryColor} className="mt-1 h-10 w-full" />
        </div>
      </div>
      <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        Save Changes
      </button>
    </div>
  )
}

function AcademicSettings() {
  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Academic Year Start</label>
        <input type="date" className="mt-1 block w-full px-3 py-2 border rounded-md" />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Current Session</label>
        <select className="mt-1 block w-full px-3 py-2 border rounded-md">
          <option>2024/2025</option>
          <option>2023/2024</option>
        </select>
      </div>
      <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        Save Changes
      </button>
    </div>
  )
}

function GradingSettings() {
  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Grading Scale</label>
        <select className="mt-1 block w-full px-3 py-2 border rounded-md">
          <option value="british_nigerian">British/Nigerian (A=70+, 5.0)</option>
          <option value="american">American (A=90+, 4.0)</option>
          <option value="custom">Custom</option>
        </select>
      </div>
      <div className="bg-gray-50 p-4 rounded">
        <h4 className="font-medium mb-2">Grade Boundaries</h4>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left">
              <th className="pb-2">Grade</th>
              <th className="pb-2">Min Score</th>
              <th className="pb-2">Points</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>A</td><td>70</td><td>5.0</td></tr>
            <tr><td>B</td><td>60</td><td>4.0</td></tr>
            <tr><td>C</td><td>50</td><td>3.0</td></tr>
            <tr><td>D</td><td>45</td><td>2.0</td></tr>
            <tr><td>F</td><td>0</td><td>0.0</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

function PaymentSettings() {
  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Payment Gateway</label>
        <select className="mt-1 block w-full px-3 py-2 border rounded-md">
          <option value="paystack">Paystack</option>
          <option value="flutterwave">Flutterwave</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Secret Key</label>
        <input type="password" className="mt-1 block w-full px-3 py-2 border rounded-md" />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Public Key</label>
        <input type="password" className="mt-1 block w-full px-3 py-2 border rounded-md" />
      </div>
      <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        Save Payment Settings
      </button>
    </div>
  )
}

function NotificationSettings() {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        {[
          { label: 'Email Notifications', desc: 'Receive important updates via email' },
          { label: 'SMS Alerts', desc: 'Get urgent notifications via SMS' },
          { label: 'Push Notifications', desc: 'Browser push notifications' },
        ].map((item) => (
          <div key={item.label} className="flex items-center justify-between p-4 border rounded">
            <div>
              <p className="font-medium">{item.label}</p>
              <p className="text-sm text-gray-500">{item.desc}</p>
            </div>
            <input type="checkbox" defaultChecked className="h-5 w-5" />
          </div>
        ))}
      </div>
      <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        Save Preferences
      </button>
    </div>
  )
}
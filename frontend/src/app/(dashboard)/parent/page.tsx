'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'

export default function ParentPortalPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()

  useEffect(() => {
    if (!isAuthenticated) router.push('/')
  }, [isAuthenticated, router])

  if (!isAuthenticated) return null

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-indigo-600 to-indigo-800 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold">Parent Portal</h1>
        <p className="text-indigo-100 mt-1">Monitor your ward's progress</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-5 shadow">
          <p className="text-sm text-gray-500">Ward Name</p>
          <p className="text-xl font-bold">Student Name</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow">
          <p className="text-sm text-gray-500">Current GPA</p>
          <p className="text-xl font-bold text-green-600">3.75</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow">
          <p className="text-sm text-gray-500">Fee Status</p>
          <p className="text-xl font-bold text-orange-600">₦50,000 Due</p>
        </div>
      </div>

      <div className="bg-white rounded-xl p-6 shadow">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-green-600 text-white rounded-lg">Pay Fees</button>
          <button className="px-4 py-2 border rounded-lg">View Results</button>
          <button className="px-4 py-2 border rounded-lg">Contact School</button>
        </div>
      </div>
    </div>
  )
}
'use client'

import { useState } from 'react'

export default function AttendancePage() {
  const [mode, setMode] = useState<'scan' | 'history'>('scan')

  const attendance = [
    { date: '2024-01-22', course: 'CSC301', status: 'Present', time: '09:00 AM' },
    { date: '2024-01-21', course: 'CSC301', status: 'Present', time: '09:00 AM' },
    { date: '2024-01-20', course: 'CSC301', status: 'Absent', time: '-' },
    { date: '2024-01-19', course: 'CSC301', status: 'Present', time: '09:15 AM' },
    { date: '2024-01-18', course: 'CSC301', status: 'Present', time: '09:00 AM' },
  ]

  const courses = [
    { code: 'CSC301', title: 'Data Structures', present: 12, total: 15, percentage: 80 },
    { code: 'MTH301', title: 'Numerical Analysis', present: 10, total: 12, percentage: 83 },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Attendance</h1>

      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setMode('scan')}
          className={`px-4 py-2 rounded ${mode === 'scan' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
        >
          Scan QR Code
        </button>
        <button
          onClick={() => setMode('history')}
          className={`px-4 py-2 rounded ${mode === 'history' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
        >
          History
        </button>
      </div>

      {mode === 'scan' && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-center py-12">
            <div className="w-64 h-64 mx-auto bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h2M4 12h2m-2 4h.01M12 20h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
            </div>
            <p className="text-gray-600 mb-4">Position camera to scan QR code</p>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Open Camera
            </button>
          </div>
        </div>
      )}

      {mode === 'history' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="font-semibold mb-4">Course Attendance</h2>
            <div className="space-y-3">
              {courses.map((course) => (
                <div key={course.code} className="border rounded p-4">
                  <div className="flex justify-between items-center mb-2">
                    <div>
                      <h3 className="font-medium">{course.code}</h3>
                      <p className="text-sm text-gray-500">{course.title}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-sm ${
                      course.percentage >= 75 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {course.percentage}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${course.percentage >= 75 ? 'bg-green-500' : 'bg-red-500'}`} 
                      style={{ width: `${course.percentage}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{course.present}/{course.total} sessions</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b">
              <h2 className="font-semibold">Attendance History</h2>
            </div>
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Course</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {attendance.map((record, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4">{record.date}</td>
                    <td className="px-6 py-4">{record.course}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs ${
                        record.status === 'Present' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {record.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-gray-500">{record.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
'use client'

import { useState, useEffect } from 'react'

export default function StudentResultsPage() {
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    try {
      const res = await fetch('/api/v1/students/me/results')
      const data = await res.json()
      setResults(data)
    } catch (error) {
      console.error('Failed to fetch results')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>

  const courses = results?.results || []

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Academic Results</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Current GPA</p>
          <p className="text-3xl font-bold text-blue-600">{results?.gpa || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Cumulative GPA</p>
          <p className="text-3xl font-bold text-green-600">{results?.cgpa || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Credits Completed</p>
          <p className="text-3xl font-bold">{results?.total_credits || 0}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h2 className="font-semibold">Course Results</h2>
        </div>
        {courses.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No results available</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Course</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Grade</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Points</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {courses.map((course: any) => (
                <tr key={course.id}>
                  <td className="px-6 py-4">{course.code}</td>
                  <td className="px-6 py-4">{course.score}</td>
                  <td className="px-6 py-4"><span className="px-2 py-1 bg-blue-100 rounded">{course.grade}</span></td>
                  <td className="px-6 py-4">{course.grade_point}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

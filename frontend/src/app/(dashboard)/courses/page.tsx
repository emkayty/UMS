'use client'

import { useState, useEffect } from 'react'

export default function StudentCoursesPage() {
  const [courses, setCourses] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCourses()
  }, [])

  const fetchCourses = async () => {
    try {
      const res = await fetch('/api/v1/students/me/courses')
      const data = await res.json()
      setCourses(data.courses || [])
    } catch (error) {
      console.error('Failed to fetch courses')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">My Courses</h1>
      {courses.length === 0 ? (
        <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
          <p className="text-yellow-800">No courses registered. Please register for courses.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {courses.map((course: any) => (
            <div key={course.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-lg">{course.code}</h3>
                  <p className="text-gray-600">{course.title}</p>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                  {course.status || 'Active'}
                </span>
              </div>
              <div className="mt-4 flex gap-2">
                <button className="flex-1 px-3 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                  Materials
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
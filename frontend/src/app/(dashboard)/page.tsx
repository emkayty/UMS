'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'

interface DashboardStats {
  totalStudents?: number
  totalStaff?: number
  totalCourses?: number
  pendingApprovals?: number
}

export default function DashboardPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [stats, setStats] = useState<DashboardStats>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
      return
    }
    fetchDashboardData()
  }, [isAuthenticated, router])

  const fetchDashboardData = async () => {
    try {
      const res = await fetch('/api/v1/reports/system/stats')
      const data = await res.json()
      setStats(data)
    } catch (error) {
      console.error('Failed to fetch stats')
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated || !user) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold">
          Welcome back, {user.first_name || user.email.split('@')[0]}!
        </h1>
        <p className="text-blue-100 mt-1">{getRoleGreeting(user.role)}</p>
        <div className="mt-4 flex gap-3">
          <span className="px-3 py-1 bg-white/20 rounded-full text-sm">{getRoleLabel(user.role)}</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {getRoleStats(user.role, stats).map((stat, idx) => (
          <StatCard key={idx} {...stat} />
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {getQuickActions(user.role).map((action, idx) => (
            <button
              key={idx}
              onClick={() => router.push(action.href)}
              className="flex flex-col items-center justify-center p-4 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all group"
            >
              <span className="text-2xl mb-2">{action.icon}</span>
              <span className="text-xs text-gray-600 text-center">{action.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Activity & Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentActivity />
        <PendingTasks />
      </div>
    </div>
  )
}

function getRoleGreeting(role: string): string {
  const greetings: Record<string, string> = {
    student: "Track your academic progress and stay on top of your courses.",
    lecturer: "Manage your courses, materials, and student progress.",
    hod: "Oversee department operations and approve requests.",
    dean: "Manage faculty-wide operations and curriculum.",
    registrar: "Handle admissions, registrations, and student records.",
    bursar: "Track finances, payments, and scholarships.",
    institution_admin: "System administration and institution settings."
  }
  return greetings[role] || "Welcome to your dashboard."
}

function getRoleLabel(role: string): string {
  const labels: Record<string, string> = {
    student: "Student", lecturer: "Lecturer", hod: "Head of Department",
    dean: "Dean", registrar: "Registrar", bursar: "Bursar", institution_admin: "Administrator"
  }
  return labels[role] || role
}

function getRoleStats(role: string, stats: DashboardStats) {
  const allStats: Record<string, any[]> = {
    student: [
      { label: 'My GPA', value: '3.75', icon: '📊', color: 'blue' },
      { label: 'Courses', value: '5', icon: '📖', color: 'green' },
      { label: 'Due Assignments', value: '2', icon: '📝', color: 'orange' },
      { label: 'Messages', value: '3', icon: '💬', color: 'purple' },
    ],
    lecturer: [
      { label: 'My Courses', value: '4', icon: '📖', color: 'blue' },
      { label: 'Pending Grades', value: '12', icon: '📝', color: 'orange' },
      { label: 'Materials', value: '8', icon: '📁', color: 'green' },
      { label: 'Students', value: '150', icon: '👥', color: 'purple' },
    ],
    hod: [
      { label: 'Pending Approvals', value: stats.pendingApprovals || 5, icon: '✅', color: 'orange' },
      { label: 'Department Staff', value: stats.totalStaff || 12, icon: '👨‍🏫', color: 'blue' },
      { label: 'Courses', value: stats.totalCourses || 24, icon: '📚', color: 'green' },
      { label: 'Leave Requests', value: '2', icon: '🏖️', color: 'purple' },
    ],
    registrar: [
      { label: 'Applications', value: '450', icon: '📝', color: 'blue' },
      { label: 'Registered', value: '850', icon: '✅', color: 'green' },
      { label: 'Graduating', value: '180', icon: '🎓', color: 'purple' },
      { label: 'Pending Clearances', value: '25', icon: '⚠️', color: 'orange' },
    ],
    bursar: [
      { label: 'Revenue', value: '₦12.5M', icon: '💰', color: 'green' },
      { label: 'Outstanding', value: '₦2.1M', icon: '💳', color: 'orange' },
      { label: 'Scholarships', value: '45', icon: '🎁', color: 'purple' },
      { label: 'Transactions', value: '120', icon: '📊', color: 'blue' },
    ],
    institution_admin: [
      { label: 'Total Users', value: stats.totalStudents || 1500, icon: '👥', color: 'blue' },
      { label: 'Active Users', value: Math.floor((stats.totalStudents || 1500) * 0.8), icon: '✅', color: 'green' },
      { label: 'Storage Used', value: '45MB', icon: '💾', color: 'orange' },
      { label: 'API Calls', value: '1.2K', icon: '🔗', color: 'purple' },
    ]
  }
  return allStats[role] || [
    { label: 'Total Students', value: stats.totalStudents || 0, icon: '👨‍🎓', color: 'blue' },
    { label: 'Total Staff', value: stats.totalStaff || 0, icon: '👨‍🏫', color: 'green' },
    { label: 'Active Courses', value: stats.totalCourses || 0, icon: '📚', color: 'purple' },
  ]
}

function getQuickActions(role: string) {
  const actions: Record<string, any[]> = {
    student: [
      { icon: '📚', label: 'My Courses', href: '/dashboard/courses' },
      { icon: '📝', label: 'Assignments', href: '/dashboard/assignments' },
      { icon: '📊', label: 'Results', href: '/dashboard/results' },
      { icon: '💰', label: 'Fees', href: '/dashboard/finance' },
      { icon: '🎓', label: 'Clearance', href: '/dashboard/clearance' },
      { icon: '📱', label: 'Attendance', href: '/dashboard/attendance' },
    ],
    lecturer: [
      { icon: '📖', label: 'My Courses', href: '/dashboard/courses' },
      { icon: '📁', label: 'Materials', href: '/dashboard/materials' },
      { icon: '📝', label: 'Grade Book', href: '/dashboard/grades' },
      { icon: '📱', label: 'Attendance', href: '/dashboard/attendance' },
    ],
    hod: [
      { icon: '✅', label: 'Approvals', href: '/dashboard/approvals' },
      { icon: '📚', label: 'Courses', href: '/dashboard/courses' },
      { icon: '👥', label: 'Staff', href: '/dashboard/staff' },
      { icon: '📅', label: 'Schedule', href: '/dashboard/schedule' },
    ],
    registrar: [
      { icon: '📝', label: 'Admissions', href: '/dashboard/admissions' },
      { icon: '👥', label: 'Records', href: '/dashboard/records' },
      { icon: '🎓', label: 'Graduation', href: '/dashboard/graduation' },
      { icon: '📅', label: 'Calendar', href: '/dashboard/calendar' },
    ],
    bursar: [
      { icon: '💰', label: 'Fees', href: '/dashboard/fees' },
      { icon: '💳', label: 'Payments', href: '/dashboard/payments' },
      { icon: '📊', label: 'Reports', href: '/dashboard/reports' },
      { icon: '🎁', label: 'Scholarships', href: '/dashboard/scholarships' },
    ],
    institution_admin: [
      { icon: '👥', label: 'Users', href: '/dashboard/users' },
      { icon: '🏗️', label: 'Structure', href: '/dashboard/structure' },
      { icon: '📊', label: 'Reports', href: '/dashboard/reports' },
      { icon: '🤖', label: 'AI Analytics', href: '/dashboard/ai' },
    ]
  }
  return actions[role] || []
}

function StatCard({ label, value, icon, color }: { label: string, value: any, icon: string, color: string }) {
  const colorClasses: Record<string, string> = {
    blue: 'from-blue-50 to-blue-100 border-blue-200',
    green: 'from-green-50 to-green-100 border-green-200',
    purple: 'from-purple-50 to-purple-100 border-purple-200',
    orange: 'from-orange-50 to-orange-100 border-orange-200',
  }
  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} border rounded-xl p-5 hover:shadow-lg transition-shadow`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </div>
  )
}

function RecentActivity() {
  const activities = [
    { icon: '📝', text: 'New assignment uploaded', time: '2 hours ago' },
    { icon: '✅', text: 'Results approved', time: '5 hours ago' },
    { icon: '🔔', text: 'Announcement posted', time: '1 day ago' },
  ]
  return (
    <div className="bg-white rounded-xl p-6">
      <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities.map((activity, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50">
            <span className="text-xl">{activity.icon}</span>
            <div>
              <p className="text-sm text-gray-900">{activity.text}</p>
              <p className="text-xs text-gray-500">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function PendingTasks() {
  const tasks = [
    { icon: '📝', text: 'Complete course registration', priority: 'high' },
    { icon: '💰', text: 'Pay outstanding fees', priority: 'high' },
    { icon: '📚', text: 'Submit assignment', priority: 'medium' },
  ]
  const priorityColors: Record<string, string> = {
    high: 'bg-red-100 text-red-700',
    medium: 'bg-yellow-100 text-yellow-700',
  }
  return (
    <div className="bg-white rounded-xl p-6">
      <h2 className="text-lg font-semibold mb-4">Pending Tasks</h2>
      <div className="space-y-3">
        {tasks.map((task, idx) => (
          <div key={idx} className="flex items-center justify-between p-3 rounded-lg border border-gray-200">
            <div className="flex items-center gap-3">
              <span className="text-xl">{task.icon}</span>
              <span className="text-sm text-gray-700">{task.text}</span>
            </div>
            <span className={`px-2 py-1 text-xs rounded-full ${priorityColors[task.priority]}`}>{task.priority}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

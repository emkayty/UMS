'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'

// Dashboard Layout Component
export default function DashboardLayout({
  children,
  role = 'student',
}: {
  children: React.ReactNode
  role?: string
}) {
  const router = useRouter()
  const { user, logout, isAuthenticated } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
    }
  }, [isAuthenticated, router])

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  const navItems = getNavItems(role)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 flex md:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button onClick={() => setSidebarOpen(false)} className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
              <span className="sr-only">Close sidebar</span>
              <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4">
              <span className="text-xl font-bold text-primary-600">UniCore</span>
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <button onClick={handleLogout} className="flex-shrink-0 w-full flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700">
              Sign out
            </button>
          </div>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden md:fixed md:inset-y-0 md:flex md:w-64 md:flex-col">
        <div className="flex-1 flex flex-col min-h-0 bg-white border-r border-gray-200">
          <div className="flex items-center h-16 px-4 border-b border-gray-200">
            <span className="text-xl font-bold text-primary-600">UniCore</span>
          </div>
          <div className="flex-1 flex flex-col overflow-y-auto">
            <nav className="flex-1 px-2 py-4 space-y-1">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="md:pl-64 flex flex-col flex-1">
        <div className="sticky top-0 z-10 flex h-16 px-4 bg-white border-b border-gray-200 md:hidden">
          <button onClick={() => setSidebarOpen(true)} className="text-gray-500 hover:text-gray-600">
            <span className="sr-only">Open sidebar</span>
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <span className="ml-4 text-lg font-semibold text-primary-600">UniCore</span>
        </div>

        <main className="flex-1">
          <div className="py-6 px-4 sm:px-6 md:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

function getNavItems(role: string) {
  const common = [
    { name: 'Dashboard', href: '/dashboard' },
  ]

  switch (role) {
    case 'student':
      return [
        ...common,
        { name: 'My Courses', href: '/dashboard/courses' },
        { name: 'Assignments', href: '/dashboard/assignments' },
        { name: 'Results', href: '/dashboard/results' },
        { name: 'Finance', href: '/dashboard/finance' },
        { name: 'Clearance', href: '/dashboard/clearance' },
      ]
    case 'lecturer':
      return [
        ...common,
        { name: 'My Courses', href: '/dashboard/courses' },
        { name: 'Materials', href: '/dashboard/materials' },
        { name: 'Grade Book', href: '/dashboard/grades' },
        { name: 'Attendance', href: '/dashboard/attendance' },
      ]
    case 'hod':
      return [
        ...common,
        { name: 'Approvals', href: '/dashboard/approvals' },
        { name: 'Course Allocation', href: '/dashboard/courses' },
        { name: 'Staff', href: '/dashboard/staff' },
      ]
    case 'dean':
      return [
        ...common,
        { name: 'Faculty', href: '/dashboard/faculty' },
        { name: 'Curriculum', href: '/dashboard/curriculum' },
        { name: 'Reports', href: '/dashboard/reports' },
      ]
    case 'registrar':
      return [
        ...common,
        { name: 'Admissions', href: '/dashboard/admissions' },
        { name: 'Records', href: '/dashboard/records' },
        { name: 'Graduation', href: '/dashboard/graduation' },
      ]
    case 'bursar':
      return [
        ...common,
        { name: 'Fees', href: '/dashboard/fees' },
        { name: 'Payments', href: '/dashboard/payments' },
        { name: 'Reports', href: '/dashboard/reports' },
      ]
    case 'institution_admin':
      return [
        ...common,
        { name: 'Users', href: '/dashboard/users' },
        { name: 'Settings', href: '/dashboard/settings' },
        { name: 'Structure', href: '/dashboard/structure' },
        { name: 'Audit Logs', href: '/dashboard/audit' },
      ]
    default:
      return common
  }
}
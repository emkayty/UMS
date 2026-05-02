import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Routes that require authentication
const protectedRoutes = ['/dashboard', '/api/v1/students', '/api/v1/lecturer', '/api/v1/fees', '/api/v1/reports']

// Routes that require specific roles
const roleBasedRoutes: Record<string, string[]> = {
  '/dashboard/admin': ['institution_admin'],
  '/dashboard/users': ['institution_admin'],
  '/dashboard/structure': ['institution_admin'],
  '/dashboard/approvals': ['hod', 'dean', 'registrar'],
  '/dashboard/admissions': ['registrar'],
  '/dashboard/graduation': ['registrar'],
  '/dashboard/fees': ['bursar'],
  '/dashboard/payments': ['bursar'],
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Check if route requires authentication
  const requiresAuth = protectedRoutes.some(route => pathname.startsWith(route))
  
  if (requiresAuth) {
    const token = request.cookies.get('access_token')?.value
    
    if (!token) {
      // Not authenticated, redirect to login
      return NextResponse.redirect(new URL('/', request.url))
    }
  }
  
  // Check role-based access
  for (const [route, roles] of Object.entries(roleBasedRoutes)) {
    if (pathname.startsWith(route)) {
      const userRole = request.cookies.get('user_role')?.value
      
      if (userRole && !roles.includes(userRole)) {
        // User doesn't have required role, redirect to dashboard
        return NextResponse.redirect(new URL('/dashboard', request.url))
      }
    }
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/v1/students/:path*',
    '/api/v1/lecturer/:path*',
    '/api/v1/fees/:path*',
    '/api/v1/reports/:path*',
  ],
}
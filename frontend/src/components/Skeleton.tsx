'use client'

interface SkeletonProps {
  className?: string
  variant?: 'text' | 'circular' | 'rectangular'
}

/**
 * Reusable skeleton loader component
 */
export function Skeleton({ className = '', variant = 'rectangular' }: SkeletonProps) {
  const baseClasses = 'animate-pulse bg-gray-200'
  
  const variants = {
    text: 'h-4 w-full rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-lg',
  }
  
  return (
    <div 
      className={`${baseClasses} ${variants[variant]} ${className}`}
      aria-hidden="true"
    />
  )
}

/**
 * Skeleton for cards
 */
export function CardSkeleton() {
  return (
    <div className="bg-white rounded-xl p-6 border border-gray-200">
      <Skeleton className="h-6 w-1/3 mb-4" variant="text" />
      <Skeleton className="h-4 w-2/3 mb-2" variant="text" />
      <Skeleton className="h-4 w-1/2" variant="text" />
    </div>
  )
}

/**
 * Skeleton for table rows
 */
export function TableRowSkeleton({ columns = 4 }: { columns?: number }) {
  return (
    <tr className="border-b border-gray-100">
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="px-4 py-3">
          <Skeleton className="h-4" variant="text" />
        </td>
      ))}
    </tr>
  )
}

/**
 * Skeleton for stats card
 */
export function StatSkeleton() {
  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 border rounded-xl p-5">
      <Skeleton className="h-4 w-20 mb-2" variant="text" />
      <Skeleton className="h-8 w-16" variant="text" />
    </div>
  )
}

/**
 * Skeleton for dashboard
 */
export function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <Skeleton className="h-32 w-full" variant="rectangular" />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => <StatSkeleton key={i} />)}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CardSkeleton />
        <CardSkeleton />
      </div>
    </div>
  )
}

/**
 * Content Skeleton for lists
 */
export function ListSkeleton({ items = 5 }: { items?: number }) {
  return (
    <div className="space-y-3">
      {[...Array(items)].map((_, i) => (
        <div key={i} className="flex items-center gap-4 p-4 bg-white rounded-lg border">
          <Skeleton className="h-10 w-10" variant="circular" />
          <div className="flex-1">
            <Skeleton className="h-4 w-1/3 mb-2" variant="text" />
            <Skeleton className="h-3 w-1/2" variant="text" />
          </div>
        </div>
      ))}
    </div>
  )
}

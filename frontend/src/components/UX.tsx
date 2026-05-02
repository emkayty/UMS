'use client'

import { ReactNode, useState, useRef } from 'react'
import { useCountUp, useFadeIn, useStagger } from '@/lib/useAnimations'

// ===== BUTTONS =====

/**
 * Pulse button with loading state
 */
export function PulseButton({ 
  children, loading, disabled, variant = 'primary', size = 'md', icon, onClick, className = '' 
}: {
  children: ReactNode
  loading?: boolean
  disabled?: boolean
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  icon?: ReactNode
  onClick?: () => void
  className?: string
}) {
  const [active, setActive] = useState(false)
  
  const base = 'inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200'
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 active:scale-95 shadow-lg shadow-blue-600/25',
    secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:scale-95 dark:bg-gray-800 dark:text-gray-100',
    ghost: 'text-gray-600 hover:bg-gray-100 active:scale-95 dark:text-gray-400 dark:hover:bg-gray-800',
  }
  const sizes = {
    sm: 'px-3 py-1.5 text-sm gap-1.5',
    md: 'px-5 py-2.5 text-base gap-2',
    lg: 'px-7 py-3.5 text-lg gap-2.5',
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      onMouseDown={() => setActive(true)}
      onMouseUp={() => setActive(false)}
      onMouseLeave={() => setActive(false)}
      className={`${base} ${variants[variant]} ${sizes[size]} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : 'active:scale-95'} ${className}`}
    >
      {loading && (
        <span className="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent" />
      )}
      {!loading && icon}
      {children}
    </button>
  )
}

/**
 * Floating action button
 */
export function FAB({ icon, onClick, className = '' }: { icon: ReactNode, onClick?: () => void, className?: string }) {
  return (
    <button
      onClick={onClick}
      className={`fixed bottom-6 right-6 w-14 h-14 rounded-full bg-blue-600 text-white shadow-xl shadow-blue-600/30 flex items-center justify-center active:scale-90 transition-transform hover:scale-110 ${className}`}
    >
      {icon}
    </button>
  )
}

// ===== CARDS =====

/**
 * Glassmorphism card
 */
export function GlassCard({ children, className = '', hover = true }: { children: ReactNode, className?: string, hover?: boolean }) {
  return (
    <div className={`backdrop-blur-xl bg-white/70 dark:bg-gray-900/70 border border-white/20 dark:border-gray-700/50 rounded-2xl ${hover ? 'hover:shadow-xl hover:border-blue-500/30 transition-all duration-300' : ''} ${className}`}>
      {children}
    </div>
  )
}

/**
 * Interactive card with flip effect
 */
export function FlipCard({ front, back }: { front: ReactNode, back: ReactNode }) {
  const [flipped, setFlipped] = useState(false)
  
  return (
    <div 
      onClick={() => setFlipped(!flipped)}
      className="relative h-64 cursor-pointer perspective-1000"
    >
      <div className={`absolute inset-0 transition-transform duration-500 transform-style-3d ${flipped ? 'rotate-y-180' : ''}`}>
        <div className="absolute inset-0 backface-hidden">
          {front}
        </div>
        <div className="absolute inset-0 backface-hidden rotate-y-180">
          {back}
        </div>
      </div>
    </div>
  )
}

// ===== INPUTS =====

/**
 * Floating label input
 */
export function FloatingInput({ 
  label, type = 'text', error, icon, className = '' 
}: {
  label: string
  type?: string
  error?: string
  icon?: ReactNode
  className?: string
}) {
  return (
    <div className={`relative ${className}`}>
      <input
        type={type}
        placeholder=" "
        className={`peer w-full px-4 pt-6 pb-2 bg-white dark:bg-gray-800 border rounded-xl outline-none transition-all
          ${error ? 'border-red-500 focus:border-red-500' : 'border-gray-200 dark:border-gray-700 focus:border-blue-500'}
          focus:ring-2 focus:ring-blue-500/20`}
      />
      <label className="absolute left-4 top-2 text-xs text-gray-500 transition-all duration-200 pointer-events-none
        peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400
        peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-500">
        {label}
      </label>
      {icon && <span className="absolute right-4 top-6 text-gray-400">{icon}</span>}
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}

/**
 * Search bar with voice
 */
export function SearchBar({ placeholder = 'Search...', onSearch, className = '' }: { 
  placeholder?: string
  onSearch?: (q: string) => void
  className?: string 
}) {
  return (
    <div className={`relative ${className}`}>
      <input
        type="search"
        placeholder={placeholder}
        className="w-full pl-12 pr-12 py-3 bg-gray-100 dark:bg-gray-800 border-0 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
      />
      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <button className="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-blue-500 transition-colors">
        🎤
      </button>
    </div>
  )
}

// ===== LOADING =====

/**
 * Shimmer loading effect
 */
export function Shimmer({ className = '' }: { className?: string }) {
  return (
    <div className={`animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] ${className}`} />
  )
}

/**
 * Dots loader
 */
export function DotsLoader({ className = '' }: { className?: string }) {
  return (
    <div className={`flex gap-1 ${className}`}>
      {[0, 1, 2].map(i => (
        <span
          key={i}
          className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  )
}

/**
 * Skeleton avatar with status
 */
export function AvatarSkeleton({ status }: { status?: 'online' | 'offline' | 'busy' }) {
  const colors = {
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    busy: 'bg-red-500',
  }
  
  return (
    <div className="relative">
      <Shimmer className="w-12 h-12 rounded-full" />
      {status && (
        <span className={`absolute bottom-0 right-0 w-3 h-3 ${colors[status]} rounded-full border-2 border-white dark:border-gray-900`} />
      )}
    </div>
  )
}

/**
 * Progress ring
 */
export function ProgressRing({ progress = 0, size = 64, strokeWidth = 4, className = '' }: {
  progress: number
  size?: number
  strokeWidth?: number
  className?: string
}) {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (progress / 100) * circumference
  
  return (
    <svg width={size} height={size} className={className}>
      <circle
        stroke="#e5e7eb"
        fill="none"
        strokeWidth={strokeWidth}
        r={radius}
        cx={size / 2}
        cy={size / 2}
      />
      <circle
        className="transition-all duration-500"
        stroke="#3b82f6"
        fill="none"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        r={radius}
        cx={size / 2}
        cy={size / 2}
        style={{
          strokeDasharray: circumference,
          strokeDashoffset: offset,
          transform: 'rotate(-90deg)',
          transformOrigin: '50% 50%',
        }}
      />
    </svg>
  )
}

// ===== EMPTY =====

/**
 * Empty state with illustration
 */
export function EmptyState({ 
  icon = '📭', title = 'Nothing here', description, action 
}: {
  icon?: string
  title: string
  description?: string
  action?: ReactNode
}) {
  const anim = useFadeIn(100)
  
  return (
    <div className={`flex flex-col items-center justify-center py-16 text-center ${anim.className}`}>
      <span className="text-6xl mb-4">{icon}</span>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
      {description && <p className="mt-2 text-gray-500 max-w-sm">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  )
}

// ===== TABS =====

/**
 * Animated tabs
 */
export function AnimatedTabs({ 
  tabs, active, onChange 
}: {
  tabs: { id: string, label: string, icon?: ReactNode }[]
  active: string
  onChange: (id: string) => void
}) {
  return (
    <div className="flex gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-xl">
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
            active === tab.id 
              ? 'text-blue-600 dark:text-blue-400' 
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          }`}
        >
          {active === tab.id && (
            <span className="absolute inset-0 bg-white dark:bg-gray-700 rounded-lg shadow-sm animate-fade-in" />
          )}
          <span className="relative flex items-center gap-2">
            {tab.icon}
            {tab.label}
          </span>
        </button>
      ))}
    </div>
  )
}

// ===== BADGES =====

/**
 * Notification badge
 */
export function NotificationBadge({ count, children }: { count: number, children: ReactNode }) {
  return (
    <div className="relative inline-flex">
      {children}
      {count > 0 && (
        <span className="absolute -top-1 -right-1 min-w-[1.25rem] h-5 flex items-center justify-center bg-red-500 text-white text-[0.625rem] font-bold rounded-full px-1 animate-pulse">
          {count > 99 ? '99+' : count}
        </span>
      )}
    </div>
  )
}

/**
 * Status badge
 */
export function StatusBadge({ 
  status, label 
}: {
  status: 'success' | 'warning' | 'error' | 'info'
  label: string
}) {
  const styles = {
    success: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    warning: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    error: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
    info: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  }
  
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}>
      {label}
    </span>
  )
}

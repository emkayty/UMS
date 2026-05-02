export interface User {
  id: string
  email: string
  role: 'student' | 'lecturer' | 'hod' | 'dean' | 'registrar' | 'bursar' | 'institution_admin'
  first_name?: string
  last_name?: string
  is_active: boolean
}

export interface AuthResponse {
  access: string
  refresh: string
  user: User
}

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// Student Types
export interface Student {
  id: string
  user_id: string
  matric_number: string
  first_name: string
  last_name: string
  email: string
  phone?: string
  programme?: Programme
  current_level: number
  admission_status: 'applied' | 'admitted' | 'registered' | 'graduated' | 'suspended'
  gender?: string
  date_of_birth?: string
  state_of_origin?: string
}

export interface Course {
  id: string
  code: string
  title: string
  credit_units: number
  level: number
  semester_offered: number
  department?: Department
  programme?: Programme
}

export interface CourseRegistration {
  id: string
  student: Student
  course: Course
  session: AcademicSession
  semester: Semester
  status: 'active' | 'dropped' | 'completed'
  registered_at: string
}

export interface Result {
  id: string
  registration: CourseRegistration
  score?: number
  grade?: string
  grade_point?: number
  status: 'pending' | 'approved' | 'rejected'
  session: AcademicSession
  semester: Semester
}

export interface CGPA {
  gpa: number
  cumulative_gpa: number
  total_credits: number
  earned_credits: number
  session: AcademicSession
}

// Academic Types
export interface Faculty {
  id: string
  name: string
  code: string
  dean?: User
}

export interface Department {
  id: string
  name: string
  code: string
  faculty: Faculty
  hod?: User
}

export interface Programme {
  id: string
  name: string
  code: string
  duration_years: number
  department: Department
}

export interface AcademicSession {
  id: string
  name: string
  start_date: string
  end_date: string
  is_current: boolean
}

export interface Semester {
  id: string
  name: string
  session: AcademicSession
  start_date: string
  end_date: string
}

// Finance Types
export interface FeeItem {
  id: string
  name: string
  amount: number
  is_compulsory: boolean
  programme?: Programme
  session?: AcademicSession
  level?: number
}

export interface StudentFee {
  id: string
  student: Student
  fee_item: FeeItem
  amount_due: number
  amount_paid: number
  status: 'pending' | 'partial' | 'paid'
}

export interface Payment {
  id: string
  student: Student
  amount: number
  payment_ref: string
  gateway: 'paystack' | 'flutterwave'
  status: 'pending' | 'success' | 'failed'
  paid_at?: string
}

// Learning Types
export interface Material {
  id: string
  course: Course
  lecturer: User
  title: string
  file_url: string
  type: 'PDF' | 'VIDEO' | 'LINK' | 'DOC'
  uploaded_at: string
  is_offline_available: boolean
}

export interface Assignment {
  id: string
  course: Course
  lecturer: User
  title: string
  description: string
  due_date: string
  max_score: number
}

export interface AttendanceSession {
  id: string
  course: Course
  lecturer: User
  date: string
  qr_code_token: string
  is_active: boolean
}

// Staff Types
export interface StaffProfile {
  id: string
  user: User
  staff_id: string
  first_name: string
  last_name: string
  department?: Department
  faculty?: Faculty
  rank: string
  employment_date: string
}

// Notification Types
export interface Notification {
  id: string
  user: User
  title: string
  message: string
  is_read: boolean
  action_url?: string
  created_at: string
}

export interface Announcement {
  id: string
  title: string
  body: string
  scope: 'global' | 'faculty' | 'department'
  faculty?: Faculty
  department?: Department
  posted_by: User
  posted_at: string
}

// AI Analytics Types
export interface RiskScore {
  student_id: string
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  dropout_risk: number
  academic_probation_risk: number
  financial_risk: number
  factors: Record<string, any>
  intervention_recommended: string[]
}

export interface GradePrediction {
  course_id: string
  predicted_score: number
  confidence: { lower: number; upper: number; confidence: number }
  score_needed: Record<string, number>
}

// Dashboard Stats
export interface DashboardStats {
  users: {
    total: number
    active: number
    students: number
    staff: number
    admin: number
  }
  academic: {
    faculties: number
    departments: number
    programmes: number
    courses: number
  }
  students: {
    total: number
    admitted: number
    registered: number
  }
  staff: {
    total: number
  }
  finance: {
    total_payments: number
    successful_payments: number
    student_fees: number
  }
}
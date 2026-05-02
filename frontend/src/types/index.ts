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

// ============================================================
// ADDITIONAL TYPES
// ============================================================

// Library Types
export interface Book {
  id: string
  isbn: string
  title: string
  author: string
  publisher: string
  year: number
  category: 'textbook' | 'reference' | 'journal'
  total_copies: number
  available_copies: number
}

export interface BookLoan {
  id: string
  book: Book
  student: Student
  borrowed_at: string
  due_date: string
  returned_at?: string
  status: 'borrowed' | 'returned' | 'overdue'
}

// Venue Types
export interface Venue {
  id: string
  name: string
  code: string
  venue_type: string
  seating_capacity: number
  building: string
}

// Timetable Types
export interface TimetableSlot {
  id: string
  course: Course
  venue?: Venue
  day: string
  start_time: string
  end_time: string
}

// Exam Types
export interface ExamSitting {
  id: string
  exam: Exam
  venue: Venue
  date: string
  start_time: string
  end_time: string
  seat_number?: string
  is_published: boolean
}

export interface Exam {
  id: string
  course: Course
  title: string
  exam_type: 'test' | 'quiz' | 'midterm' | 'final'
  date: string
  start_time: string
  duration_minutes: number
}

// Invigilation
export interface Invigilation {
  id: string
  exam: Exam
  venue: Venue
  invigilator: StaffProfile
  is_principal: boolean
  status: 'assigned' | 'completed'
}

// Disciplinary Types
export interface DisciplinaryCase {
  id: string
  student: Student
  incident_date: string
  category: string
  description: string
  status: 'reported' | 'investigating' | 'decided' | 'closed'
  created_at: string
}

export interface DisciplinaryHearing {
  id: string
  case: DisciplinaryCase
  hearing_date: string
  venue: string
  decision?: string
}

// ICT Types
export interface ITAsset {
  id: string
  asset_tag: string
  name: string
  asset_type: string
  serial_number?: string
  status: 'available' | 'in_use' | 'maintenance'
  assigned_to?: User
}

export interface ITSupportTicket {
  id: string
  title: string
  description: string
  category: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  status: 'open' | 'in_progress' | 'resolved' | 'closed'
  created_at: string
}

// Sports Types
export interface SportsTeam {
  id: string
  name: string
  sport: string
  coach?: StaffProfile
  captain?: Student
  status: 'active' | 'inactive'
}

export interface SportsFacility {
  id: string
  name: string
  type: string
  capacity: number
}

// Awards Types
export interface StudentAward {
  id: string
  name: string
  award_type: string
  amount: number
  criteria?: string
}

export interface AwardRecipient {
  id: string
  award: StudentAward
  student: Student
  amount: number
  status: 'pending' | 'approved' | 'disbursed'
}

// Enterprise Types
export interface CustomField {
  id: string
  name: string
  field_type: string
  model: string
  required: boolean
  options?: string[]
}

export interface Webhook {
  id: string
  name: string
  url: string
  events: string[]
  is_active: boolean
}

export interface APIKey {
  id: string
  name: string
  key: string
  is_active: boolean
  last_used?: string
}

// Notification Types
export interface NotificationTemplate {
  id: string
  name: string
  channel: 'email' | 'sms' | 'push'
  subject?: string
  body: string
}

// ============================================================
// FORM TYPES
// ============================================================

export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  first_name: string
  last_name: string
  email: string
  phone: string
  password: string
  confirm_password: string
}

export interface ProfileForm {
  first_name: string
  last_name: string
  phone: string
  date_of_birth?: string
  address?: string
  state?: string
}

export interface CourseRegistrationForm {
  courses: string[]
}

export interface PaymentForm {
  amount: number
  gateway: string
}

export interface TicketForm {
  title: string
  description: string
  category: string
  priority: string
}

// ============================================================
// OPTIONS TYPES
// ============================================================

export interface SelectOption {
  value: string
  label: string
}

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
  render?: (value: any, row: any) => React.ReactNode
}

export interface TableConfig {
  columns: TableColumn[]
  dataKey: string
}
# UniCore - Complete API Integration

Quick reference for all API endpoints:

## Authentication
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh  
- GET /api/v1/auth/me

## Students
- GET /api/v1/students/me/courses
- GET /api/v1/students/me/results
- GET /api/v1/students/me/fees
- GET /api/v1/students/me/clearance
- GET /api/v1/students/me/hostel
- POST /api/v1/students/apply
- GET /api/v1/students/applicants
- GET /api/v1/students/hostels
- GET /api/v1/students/change-requests
- GET /api/v1/students/discipline-records
- GET /api/v1/students/alumni

## Academic  
- GET /api/v1/academic/faculties
- GET /api/v1/academic/departments
- GET /api/v1/academic/programmes
- GET /api/v1/academic/courses
- GET /api/v1/academic/grading-policies
- GET /api/v1/academic/sessions
- GET /api/v1/academic/prerequisites

## Finance
- GET /api/v1/fees
- POST /api/v1/fees
- GET /api/v1/fees/student-fees/{id}
- POST /api/v1/payments/initialize
- GET /api/v1/payments/verify
- GET /api/v1/payments/history

## Staff
- GET /api/v1/staff
- POST /api/v1/staff
- GET /api/v1/staff/{id}/profile
- POST /api/v1/staff/{id}/leave
- GET /api/v1/staff/{id}/leaves

## Reports
- GET /api/v1/reports/student-list
- GET /api/v1/reports/staff-list  
- GET /api/v1/reports/course-list
- GET /api/v1/reports/finance-summary
- GET /api/v1/reports/academic-stats
- GET /api/v1/reports/clearance-status
- GET /api/v1/reports/system/stats
- GET /api/v1/reports/export/nysc
- GET /api/v1/reports/export/nuc-accreditation

## AI Analytics
- GET /api/v1/ai/students/{id}/risk-score
- GET /api/v1/ai/students/{id}/grade-predictions
- POST /api/v1/ai/chat
- GET /api/v1/ai/search

## Settings
- GET /api/v1/settings
- PATCH /api/v1/settings

## Announcements
- GET /api/v1/announcements
- POST /api/v1/announcements

## Notifications
- GET /api/v1/notifications
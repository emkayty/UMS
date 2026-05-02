'use client'

import { useState } from 'react'

export default function ReportsPage() {
  const [reportType, setReportType] = useState('students')

  const reportTypes = [
    { id: 'students', name: 'Student Reports' },
    { id: 'staff', name: 'Staff Reports' },
    { id: 'academic', name: 'Academic Reports' },
    { id: 'finance', name: 'Finance Reports' },
    { id: 'nysc', name: 'NYSC Reports' },
    { id: 'nuc', name: 'NUC Accreditation' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Reports & Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {reportTypes.map((type) => (
          <button
            key={type.id}
            onClick={() => setReportType(type.id)}
            className={`p-6 rounded-lg border-2 transition ${
              reportType === type.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <h3 className="font-semibold">{type.name}</h3>
          </button>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        {reportType === 'students' && <StudentReports />}
        {reportType === 'staff' && <StaffReports />}
        {reportType === 'academic' && <AcademicReports />}
        {reportType === 'finance' && <FinanceReports />}
        {reportType === 'nysc' && <NYSCReports />}
        {reportType === 'nuc' && <NUCReports />}
      </div>
    </div>
  )
}

function StudentReports() {
  const reports = [
    { name: 'Student List', description: 'All enrolled students', format: 'PDF, Excel' },
    { name: 'Admission Report', description: 'Application and admission statistics', format: 'PDF' },
    { name: 'Registration Report', description: 'Course registration status', format: 'PDF, Excel' },
    { name: 'Results Summary', description: 'Semester results overview', format: 'PDF' },
    { name: 'CGPA Report', description: 'Grade point averages', format: 'Excel' },
    { name: 'Clearance Report', description: 'Graduation clearance status', format: 'PDF' },
  ]

  return <ReportList reports={reports} />
}

function StaffReports() {
  const reports = [
    { name: 'Staff Directory', description: 'All staff members', format: 'PDF, Excel' },
    { name: 'Leave Report', description: 'Staff leave status', format: 'PDF' },
    { name: 'Workload Report', description: 'Teaching load distribution', format: 'Excel' },
    { name: 'Appraisal Report', description: 'Performance appraisal summary', format: 'PDF' },
  ]

  return <ReportList reports={reports} />
}

function AcademicReports() {
  const reports = [
    { name: 'Course List', description: 'All courses by programme', format: 'PDF, Excel' },
    { name: 'Timetable Report', description: 'Weekly timetable', format: 'PDF' },
    { name: 'Attendance Report', description: 'Attendance statistics', format: 'Excel' },
    { name: 'Grade Distribution', description: 'Grade analysis by course', format: 'PDF' },
  ]

  return <ReportList reports={reports} />
}

function FinanceReports() {
  const reports = [
    { name: 'Fee Collection', description: 'Fee payment summary', format: 'PDF, Excel' },
    { name: 'Debtors List', description: 'Outstanding fees', format: 'Excel' },
    { name: 'Income Statement', description: 'Revenue report', format: 'PDF' },
    { name: 'Scholarship Report', description: 'Scholarship disbursement', format: 'PDF, Excel' },
  ]

  return <ReportList reports={reports} />
}

function NYSCReports() {
  const reports = [
    { name: 'Mobilization List', description: 'NYSC mobilization data', format: 'Excel' },
    { name: 'Graduation List', description: 'Eligible graduates', format: 'PDF, Excel' },
    { name: 'Degree Classification', description: 'Class of degree', format: 'Excel' },
  ]

  return <ReportList reports={reports} />
}

function NUCReports() {
  const reports = [
    { name: 'Accreditation Status', description: 'Programme accreditation', format: 'PDF' },
    { name: 'Staff Qualifications', description: 'Staff credentials', format: 'PDF' },
    { name: 'Student-Staff Ratio', description: 'Ratio by department', format: 'PDF' },
    { name: 'Course Delivery', description: 'Contact hours report', format: 'PDF' },
  ]

  return <ReportList reports={reports} />
}

function ReportList({ reports }: { reports: { name: string; description: string; format: string }[] }) {
  return (
    <div className="space-y-3">
      {reports.map((report, idx) => (
        <div key={idx} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
          <div>
            <h3 className="font-medium">{report.name}</h3>
            <p className="text-sm text-gray-500">{report.description}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-gray-400">{report.format}</span>
            <button className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200">
              Generate
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
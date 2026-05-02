'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

type Step = 1 | 2 | 3 | 4 | 5

export default function SetupPage() {
  const router = useRouter()
  const [step, setStep] = useState<Step>(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  // Form data
  const [formData, setFormData] = useState({
    // Step 1
    institution_name: '',
    motto: '',
    logo_url: '',
    primary_color: '#1e3a8a',
    secondary_color: '#059669',
    // Step 2
    grading_scale_type: 'british_nigerian',
    // Step 3
    academic_year_start: '',
    semester_structure: [
      { name: 'First Semester', duration_weeks: 16 },
      { name: 'Second Semester', duration_weeks: 16 },
    ],
    // Step 4
    admin_email: '',
    admin_password: '',
    // Step 5
    payment_gateway: 'paystack',
    paystack_secret_key: '',
    paystack_public_key: '',
  })

  const updateField = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleNext = () => {
    if (step < 5) setStep((step + 1) as Step)
  }

  const handleBack = () => {
    if (step > 1) setStep((step - 1) as Step)
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    
    try {
      const res = await fetch('/api/v1/settings/setup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      
      const data = await res.json()
      
      if (data.success) {
        router.push('/')
      } else {
        setError(data.error || 'Setup failed')
      }
    } catch (err: any) {
      setError(err.message || 'Setup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12">
      <div className="max-w-xl w-full p-8 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-2">Setup Wizard</h1>
        <p className="text-gray-600 text-center mb-8">Step {step} of 5</p>

        {/* Progress bar */}
        <div className="mb-8">
          <div className="h-2 bg-gray-200 rounded-full">
            <div 
              className="h-2 bg-primary-600 rounded-full transition-all"
              style={{ width: `${(step / 5) * 100}%` }}
            />
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">
            {error}
          </div>
        )}

        {/* Step content */}
        {step === 1 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Institution Branding</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700">Institution Name *</label>
              <input
                type="text"
                value={formData.institution_name}
                onChange={(e) => updateField('institution_name', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Motto</label>
              <input
                type="text"
                value={formData.motto}
                onChange={(e) => updateField('motto', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Primary Color</label>
                <input
                  type="color"
                  value={formData.primary_color}
                  onChange={(e) => updateField('primary_color', e.target.value)}
                  className="mt-1 block w-full h-10"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Secondary Color</label>
                <input
                  type="color"
                  value={formData.secondary_color}
                  onChange={(e) => updateField('secondary_color', e.target.value)}
                  className="mt-1 block w-full h-10"
                />
              </div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Grading System</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700">Scale Type</label>
              <select
                value={formData.grading_scale_type}
                onChange={(e) => updateField('grading_scale_type', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="british_nigerian">British/Nigerian (A=70+, 5.0 scale)</option>
                <option value="american">American (A=90+, 4.0 scale)</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            {formData.grading_scale_type === 'british_nigerian' && (
              <div className="p-4 bg-gray-50 rounded-md text-sm">
                <p className="font-medium mb-2">Grading Scale:</p>
                <ul className="space-y-1 text-gray-600">
                  <li>A: 70-100% (5.0)</li>
                  <li>B: 60-69% (4.0)</li>
                  <li>C: 50-59% (3.0)</li>
                  <li>D: 45-49% (2.0)</li>
                  <li>E: 40-44% (1.0)</li>
                  <li>F: 0-39% (0.0)</li>
                </ul>
              </div>
            )}
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Academic Calendar</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700">Academic Year Start *</label>
              <input
                type="date"
                value={formData.academic_year_start}
                onChange={(e) => updateField('academic_year_start', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div className="p-4 bg-gray-50 rounded-md">
              <p className="text-sm text-gray-600">Semester structure will be auto-configured based on start date</p>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Administrator Account</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700">Admin Email *</label>
              <input
                type="email"
                value={formData.admin_email}
                onChange={(e) => updateField('admin_email', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Password *</label>
              <input
                type="password"
                value={formData.admin_password}
                onChange={(e) => updateField('admin_password', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                minLength={8}
                required
              />
            </div>
          </div>
        )}

        {step === 5 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Payment Gateway</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700">Gateway</label>
              <select
                value={formData.payment_gateway}
                onChange={(e) => updateField('payment_gateway', e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="paystack">Paystack</option>
                <option value="flutterwave">Flutterwave</option>
              </select>
            </div>
            {formData.payment_gateway === 'paystack' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Secret Key</label>
                  <input
                    type="password"
                    value={formData.paystack_secret_key}
                    onChange={(e) => updateField('paystack_secret_key', e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Public Key</label>
                  <input
                    type="password"
                    value={formData.paystack_public_key}
                    onChange={(e) => updateField('paystack_public_key', e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>
              </>
            )}
          </div>
        )}

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8">
          <button
            type="button"
            onClick={handleBack}
            disabled={step === 1}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Back
          </button>
          
          {step < 5 ? (
            <button
              type="button"
              onClick={handleNext}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              Next
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Setting up...' : 'Complete Setup'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
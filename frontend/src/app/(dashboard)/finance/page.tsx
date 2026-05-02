'use client'

import { useState, useEffect } from 'react'

export default function StudentFinancePage() {
  const [fees, setFees] = useState<any>(null)
  const [payments, setPayments] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFinance()
  }, [])

  const fetchFinance = async () => {
    try {
      const [feesRes, paymentsRes] = await Promise.all([
        fetch('/api/v1/fees/student-fees/me'),
        fetch('/api/v1/payments/history')
      ])
      const feesData = await feesRes.json()
      const paymentsData = await paymentsRes.json()
      setFees(feesData)
      setPayments(paymentsData.payments || [])
    } catch (error) {
      console.error('Failed to fetch finance data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>

  const feeItems = fees?.fees || []
  const totalDue = feeItems.reduce((sum: number, f: any) => sum + (f.amount_due || 0), 0)
  const totalPaid = feeItems.reduce((sum: number, f: any) => sum + (f.amount_paid || 0), 0)
  const balance = totalDue - totalPaid

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Finance</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Total Due</p>
          <p className="text-2xl font-bold">${totalDue.toLocaleString()}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Amount Paid</p>
          <p className="text-2xl font-bold text-green-600">${totalPaid.toLocaleString()}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-sm">Balance</p>
          <p className="text-2xl font-bold text-red-600">${balance.toLocaleString()}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="font-semibold">Fee Items</h2>
        </div>
        {feeItems.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No fee items</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left">Item</th>
                <th className="px-4 py-2 text-right">Amount</th>
                <th className="px-4 py-2 text-right">Paid</th>
                <th className="px-4 py-2 text-left">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {feeItems.map((fee: any, idx: number) => (
                <tr key={idx}>
                  <td className="px-4 py-3">{fee.name}</td>
                  <td className="px-4 py-3 text-right">${(fee.amount_due || 0).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right">${(fee.amount_paid || 0).toLocaleString()}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs rounded ${fee.status === 'paid' ? 'bg-green-100' : 'bg-red-100'}`}>
                      {fee.status || 'pending'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="bg-white rounded-lg shadow mt-6">
        <div className="px-6 py-4 border-b">
          <h2 className="font-semibold">Payment History</h2>
        </div>
        {payments.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No payments yet</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left">Date</th>
                <th className="px-4 py-2 text-left">Description</th>
                <th className="px-4 py-2 text-right">Amount</th>
                <th className="px-4 py-2 text-left">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {payments.map((payment: any, idx: number) => (
                <tr key={idx}>
                  <td className="px-4 py-3">{payment.date || payment.paid_at}</td>
                  <td className="px-4 py-3">{payment.description}</td>
                  <td className="px-4 py-3 text-right">${(payment.amount || 0).toLocaleString()}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-1 text-xs rounded bg-green-100">{payment.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

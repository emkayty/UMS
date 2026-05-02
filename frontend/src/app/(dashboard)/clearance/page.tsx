'use client'

export default function ClearancePage() {
  const clearance = [
    { name: 'Library', status: 'Cleared', date: '2024-01-20' },
    { name: 'Bursary', status: 'Cleared', date: '2024-01-18' },
    { name: 'Hostel', status: 'Pending', date: null },
    { name: 'Department', status: 'Cleared', date: '2024-01-22' },
  ]

  const completed = clearance.filter(c => c.status === 'Cleared').length
  const progress = (completed / clearance.length) * 100

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Graduation Clearance</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="font-semibold">Clearance Progress</h2>
          <span className="text-2xl font-bold text-blue-600">{completed}/{clearance.length}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div className="bg-blue-600 h-4 rounded-full transition-all" style={{ width: `${progress}%` }}></div>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          {progress === 100 ? 'You are eligible to graduate!' : 'Complete all clearance requirements to graduate.'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {clearance.map((item) => (
          <div key={item.name} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold">{item.name}</h3>
                <p className="text-sm text-gray-500">{item.date || 'Pending'}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm ${
                item.status === 'Cleared' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {item.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      {progress === 100 && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="font-semibold text-green-800 mb-2">Congratulations!</h3>
          <p className="text-green-700 mb-4">You have completed all clearance requirements and are eligible to graduate.</p>
          <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
            Request Transcript
          </button>
        </div>
      )}
    </div>
  )
}
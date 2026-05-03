'use client';
export default function StaffPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Staff Management</h1>
      
      <div className="grid gap-6 md:grid-cols-3">
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Staff Directory</h2>
          <p className="text-gray-600">View all staff members</p>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Leave Management</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mt-2">
            Request Leave
          </button>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Attendance</h2>
          <button className="bg-green-600 text-white px-4 py-2 rounded mt-2">
            Check In
          </button>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Payroll</h2>
          <p className="text-gray-600">View salary slips</p>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Performance</h2>
          <p className="text-gray-600">Appraisal records</p>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">ID Card</h2>
          <button className="bg-purple-600 text-white px-4 py-2 rounded mt-2">
            Request ID
          </button>
        </div>
      </div>
    </div>
  );
}
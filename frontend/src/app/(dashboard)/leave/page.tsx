'use client';
export default function LeavePage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Leave Management</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Leave Balance</h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-gray-100 p-3 rounded">
              <p className="text-2xl font-bold">14</p>
              <p className="text-sm">Annual</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <p className="text-2xl font-bold">7</p>
              <p className="text-sm">Sick</p>
            </div>
            <div className="bg-gray-100 p-3 rounded">
              <p className="text-2xl font-bold">3</p>
              <p className="text-sm">Casual</p>
            </div>
          </div>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Apply for Leave</h2>
          <form className="space-y-4">
            <div>
              <label className="block text-sm mb-1">Leave Type</label>
              <select className="border p-2 rounded w-full">
                <option>Annual Leave</option>
                <option>Sick Leave</option>
                <option>Casual Leave</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-sm mb-1">Start Date</label>
                <input type="date" className="border p-2 rounded w-full" />
              </div>
              <div>
                <label className="block text-sm mb-1">End Date</label>
                <input type="date" className="border p-2 rounded w-full" />
              </div>
            </div>
            <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">
              Submit Application
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
'use client';
export default function IDCardsPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">ID Card Management</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Request New ID Card</h2>
          <form className="space-y-4">
            <div>
              <label className="block text-sm mb-1">Reason</label>
              <select className="border p-2 rounded w-full">
                <option>New Student</option>
                <option>Lost Card</option>
                <option>Damaged Card</option>
                <option>Name Change</option>
              </select>
            </div>
            <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">
              Submit Request
            </button>
          </form>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">My ID Card</h2>
          <div className="border-2 border-gray-300 rounded-lg p-4 text-center">
            <div className="bg-gray-200 h-32 w-24 mx-auto mb-2"></div>
            <p className="font-bold">JOHN DOE</p>
            <p className="text-sm">STU/2024/001</p>
            <p className="text-sm text-gray-600">ND Computer Science</p>
          </div>
          <button className="bg-green-600 text-white px-4 py-2 rounded w-full mt-2">
            Download PDF
          </button>
        </div>
      </div>
    </div>
  );
}
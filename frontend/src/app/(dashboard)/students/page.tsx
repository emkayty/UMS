'use client';
export default function StudentsPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Student Management</h1>
      
      <div className="mb-4 flex gap-2">
        <input 
          type="text" 
          placeholder="Search students..." 
          className="border p-2 rounded flex-1"
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">
          Search
        </button>
      </div>
      
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">ID</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Program</th>
              <th className="p-3 text-left">Level</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t">
              <td className="p-3">STU001</td>
              <td className="p-3">John Doe</td>
              <td className="p-3">ND Computer Science</td>
              <td className="p-3">ND II</td>
              <td className="p-3"><span className="green px-2 py-1 rounded text-sm">Active</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
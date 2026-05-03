'use client';
export default function SIWESPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">SIWES / IT Placement</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">My Placements</h2>
          <div className="space-y-2">
            <div className="border p-3 rounded">
              <p className="font-medium">Tech Solutions Ltd</p>
              <p className="text-sm text-gray-600">Status: Approved</p>
              <p className="text-sm">Jan 15 - Apr 15, 2025</p>
            </div>
          </div>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Logbook</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            Update Logbook
          </button>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Companies</h2>
          <div className="space-y-2">
            <div className="border p-3 rounded">
              <p className="font-medium">Global Tech Inc</p>
              <button className="text-blue-600 text-sm">Apply</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
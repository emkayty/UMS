'use client';
export default function AlumniPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Alumni Portal</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">My Profile</h2>
          <p className="text-gray-600">Update your alumni information</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mt-2">
            Edit Profile
          </button>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Upcoming Events</h2>
          <div className="space-y-2">
            <div className="border p-3 rounded">
              <p className="font-medium">Class of 2024 Reunion</p>
              <p className="text-sm text-gray-600">June 15, 2025</p>
            </div>
          </div>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Job Board</h2>
          <div className="space-y-2">
            <div className="border p-3 rounded">
              <p className="font-medium">Software Engineer - TechCorp</p>
              <button className="text-blue-600 text-sm">Apply</button>
            </div>
          </div>
        </div>
        
        <div className="border p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Directory</h2>
          <button className="bg-gray-600 text-white px-4 py-2 rounded">
            Search Alumni
          </button>
        </div>
      </div>
    </div>
  );
}
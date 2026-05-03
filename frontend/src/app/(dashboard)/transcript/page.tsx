'use client';
export default function TranscriptPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Transcript Request</h1>
      <div className="border p-6 rounded-lg max-w-lg">
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Student ID</label>
            <input type="text" className="border p-2 rounded w-full" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Program</label>
            <select className="border p-2 rounded w-full">
              <option>ND</option>
              <option>HND</option>
              <option>BSc</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Destination Institution</label>
            <input type="text" className="border p-2 rounded w-full" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Purpose</label>
            <select className="border p-2 rounded w-full">
              <option>Further Studies</option>
              <option>Employment</option>
              <option>Verification</option>
            </select>
          </div>
          <button className="bg-blue-600 text-white px-6 py-2 rounded w-full">
            Submit Request
          </button>
        </form>
      </div>
    </div>
  );
}
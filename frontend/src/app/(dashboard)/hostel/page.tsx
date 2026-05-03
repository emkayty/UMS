'use client';
import { useState } from 'react';
import api from '@/lib/api';

export default function HostelPage() {
  const [hostels, setHostels] = useState<any[]>([]);
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Hostel Management</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="border p-4 rounded-lg">
          <h2 className="font-semibold">Male Hostel</h2>
          <p className="text-gray-600">50 beds available</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mt-2">
            Apply Now
          </button>
        </div>
        <div className="border p-4 rounded-lg">
          <h2 className="font-semibold">Female Hostel</h2>
          <p className="text-gray-600">35 beds available</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mt-2">
            Apply Now
          </button>
        </div>
      </div>
    </div>
  );
}

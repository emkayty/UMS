'use client';
import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Hostel {
  id: number;
  name: string;
  total_beds: number;
  available_beds: number;
  gender: string;
}

export default function HostelPage() {
  const [hostels, setHostels] = useState<Hostel[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadHostels();
  }, []);
  
  const loadHostels = async () => {
    try {
      const result = await api.hostelApi.list();
      if (result.success && result.data) {
        setHostels(result.data);
      }
    } catch (error) {
      console.error('Failed to load hostels:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleApply = async (hostelId: number) => {
    const result = await api.hostelApi.apply({ hostel_id: hostelId });
    alert(result.success ? 'Application submitted!' : 'Failed to apply');
  };
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Hostel Management</h1>
      {loading ? (
        <p className="text-gray-600">Loading...</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {hostels.length > 0 ? (
            hostels.map((hostel) => (
              <div key={hostel.id} className="border p-4 rounded-lg">
                <h2 className="font-semibold">{hostel.name}</h2>
                <p className="text-gray-600">{hostel.available_beds} beds available</p>
                <p className="text-sm text-gray-500">Gender: {hostel.gender}</p>
                <button 
                  className="bg-blue-600 text-white px-4 py-2 rounded mt-2"
                  onClick={() => handleApply(hostel.id)}
                >
                  Apply Now
                </button>
              </div>
            ))
          ) : (
            <>
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
            </>
          )}
        </div>
      )}
    </div>
  );
}

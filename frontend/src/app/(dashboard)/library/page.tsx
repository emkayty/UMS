'use client';
import { useState } from 'react';
import api from '@/lib/api';

export default function LibraryPage() {
  const [books, setBooks] = useState<any[]>([]);
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Library</h1>
      
      <div className="mb-4">
        <input 
          type="text" 
          placeholder="Search books..." 
          className="border p-2 rounded w-full"
        />
      </div>
      
      <div className="grid gap-4 md:grid-cols-3">
        <div className="border p-4 rounded-lg">
          <h2 className="font-semibold">Introduction to Algorithms</h2>
          <p className="text-gray-600">Available</p>
          <button className="bg-green-600 text-white px-4 py-2 rounded mt-2">
            Borrow
          </button>
        </div>
        <div className="border p-4 rounded-lg">
          <h2 className="font-semibold">Data Structures</h2>
          <p className="text-gray-600">Available</p>
          <button className="bg-green-600 text-white px-4 py-2 rounded mt-2">
            Borrow
          </button>
        </div>
        <div className="border p-4 rounded-lg">
          <h2 className="font-semibold">Database Systems</h2>
          <p className="text-gray-600">Borrowed</p>
          <button className="bg-gray-400 text-white px-4 py-2 rounded mt-2" disabled>
            Reserve
          </button>
        </div>
      </div>
    </div>
  );
}
'use client';
import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  available: boolean;
}

export default function LibraryPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadBooks();
  }, []);
  
  const loadBooks = async () => {
    try {
      const result = await api.libApi.books();
      if (result.success && result.data) {
        setBooks(result.data);
      }
    } catch (error) {
      console.error('Failed to load books:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleBorrow = async (bookId: number) => {
    const result = await api.libApi.borrow({ book_id: bookId });
    alert(result.success ? 'Book borrowed!' : 'Failed to borrow');
  };
  
  const filteredBooks = books.filter(b => 
    b.title.toLowerCase().includes(search.toLowerCase()) ||
    b.author.toLowerCase().includes(search.toLowerCase())
  );
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Library</h1>
      
      <div className="mb-4">
        <input 
          type="text" 
          placeholder="Search books..."
          className="border p-2 rounded w-full"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-3">
          {filteredBooks.length > 0 ? (
            filteredBooks.map((book) => (
              <div key={book.id} className="border p-4 rounded-lg">
                <h2 className="font-semibold">{book.title}</h2>
                <p className="text-gray-600">{book.author}</p>
                <p className="text-sm text-gray-500">ISBN: {book.isbn}</p>
                <button 
                  className={book.available ? "bg-green-600" : "bg-gray-400"}
                  disabled={!book.available}
                  onClick={() => handleBorrow(book.id)}
                >
                  {book.available ? 'Borrow' : 'Reserved'}
                </button>
              </div>
            ))
          ) : (
            <p>No books found</p>
          )}
        </div>
      )}
    </div>
  );
}
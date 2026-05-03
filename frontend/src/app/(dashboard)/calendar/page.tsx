'use client';
export default function CalendarPage() {
  const events = [
    { id: 1, title: 'Mid-Semester Exams', date: 'June 10-15', type: 'exam' },
    { id: 2, title: 'Lecture Break', date: 'June 16-20', type: 'break' },
    { id: 3, title: 'Semester Exam', date: 'July 1-15', type: 'exam' },
  ];
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Academic Calendar</h1>
      <div className="space-y-4">
        {events.map(e => (
          <div key={e.id} className="border p-4 rounded-lg flex justify-between items-center">
            <div>
              <h3 className="font-semibold">{e.title}</h3>
              <p className="text-gray-600">{e.date}</p>
            </div>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              {e.type}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
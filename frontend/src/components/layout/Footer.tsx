export default function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center text-sm text-gray-500">
          <p>&copy; 2026 ReferIn. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-indigo-600">About</a>
            <a href="#" className="hover:text-indigo-600">Privacy</a>
            <a href="#" className="hover:text-indigo-600">Terms</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

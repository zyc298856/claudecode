export function Footer() {
  return (
    <footer className="border-t border-gray-200 mt-16">
      <div className="max-w-3xl mx-auto px-4 py-6 text-center text-sm text-gray-500">
        <p>&copy; {new Date().getFullYear()} My Tech Blog. Built with Next.js.</p>
      </div>
    </footer>
  );
}

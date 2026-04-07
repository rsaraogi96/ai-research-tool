import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Command } from 'lucide-react';

export default function Header() {
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      setSearchOpen(true);
    }
    if (e.key === 'Escape') {
      setSearchOpen(false);
    }
  }, []);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
      setSearchOpen(false);
      setQuery('');
    }
  };

  return (
    <>
      <header className="h-14 border-b border-border bg-bg-secondary/80 backdrop-blur-sm flex items-center px-6 sticky top-0 z-40">
        <button
          onClick={() => setSearchOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-bg-card border border-border text-text-muted text-sm hover:border-accent-blue/50 hover:text-text-secondary transition-all w-72"
        >
          <Search className="w-4 h-4" />
          <span className="flex-1 text-left">Search research...</span>
          <kbd className="hidden sm:flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-bg-primary text-xs font-mono">
            <Command className="w-3 h-3" />K
          </kbd>
        </button>
      </header>

      {/* Search Modal */}
      {searchOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setSearchOpen(false)} />
          <div className="relative w-full max-w-xl bg-bg-card border border-border rounded-xl shadow-2xl shadow-black/50 overflow-hidden">
            <form onSubmit={handleSearch}>
              <div className="flex items-center gap-3 px-4 border-b border-border">
                <Search className="w-5 h-5 text-accent-cyan" />
                <input
                  autoFocus
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search papers, blogs, topics..."
                  className="flex-1 py-4 bg-transparent text-text-primary outline-none text-base placeholder:text-text-muted"
                />
                <kbd className="px-2 py-0.5 rounded bg-bg-primary text-xs text-text-muted font-mono">ESC</kbd>
              </div>
            </form>
            <div className="px-4 py-3 text-xs text-text-muted">
              Press Enter to search, or type a query and hit Enter
            </div>
          </div>
        </div>
      )}
    </>
  );
}

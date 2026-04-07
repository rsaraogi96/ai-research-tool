import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Search as SearchIcon, Filter } from 'lucide-react';
import { apiGet, type SearchResponse } from '@/api/client';
import { sourceLabel, timeAgo } from '@/lib/utils';

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState<SearchResponse | null>(null);
  const [input, setInput] = useState(searchParams.get('q') || '');
  const [loading, setLoading] = useState(false);

  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');

  useEffect(() => {
    if (!query) return;
    setLoading(true);
    apiGet<SearchResponse>('/search', { q: query, page, per_page: 20 })
      .then(setData)
      .finally(() => setLoading(false));
  }, [query, page]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      setSearchParams({ q: input.trim() });
    }
  };

  return (
    <div className="space-y-6">
      {/* Search Input */}
      <form onSubmit={handleSearch} className="flex gap-3">
        <div className="flex-1 flex items-center gap-3 px-4 py-3 rounded-xl bg-bg-card border border-border focus-within:border-accent-cyan/50 focus-within:shadow-[0_0_15px_rgba(6,182,212,0.15)] transition-all">
          <SearchIcon className="w-5 h-5 text-accent-cyan" />
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Search papers, topics, companies..."
            className="flex-1 bg-transparent text-text-primary outline-none text-base placeholder:text-text-muted"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-3 rounded-xl bg-accent-blue/20 border border-accent-blue/40 text-accent-cyan font-medium hover:bg-accent-blue/30 transition-all"
        >
          Search
        </button>
      </form>

      {/* Results */}
      {data && (
        <div className="grid grid-cols-4 gap-6">
          {/* Main Results */}
          <div className="col-span-3 space-y-3">
            <p className="text-sm text-text-muted">
              {data.total} results for "<span className="text-accent-cyan">{data.query}</span>"
            </p>
            {data.results.map(({ instance: item, title_snippet, description_snippet, relevance_score }) => (
              <Link
                key={item.id}
                to={`/instance/${item.id}`}
                className="glow-card p-4 block group"
              >
                <div className="flex items-start gap-3">
                  <div className={`w-2.5 h-2.5 rounded-full mt-1.5 flex-shrink-0 source-dot-${item.source_type}`} />
                  <div className="flex-1">
                    <h3
                      className="text-sm font-medium text-text-primary group-hover:text-accent-cyan transition-colors"
                      dangerouslySetInnerHTML={{ __html: title_snippet || item.title }}
                    />
                    {(description_snippet || item.description) && (
                      <p
                        className="text-xs text-text-muted mt-1 line-clamp-2"
                        dangerouslySetInnerHTML={{ __html: description_snippet || item.description || '' }}
                      />
                    )}
                    <div className="flex items-center gap-3 mt-2">
                      <span className={`text-xs source-${item.source_type}`}>{sourceLabel(item.source_type)}</span>
                      {item.company && <span className="text-xs text-text-secondary">{item.company.name}</span>}
                      {item.industry && <span className="badge badge-industry text-[10px]">{item.industry}</span>}
                      {item.domain && <span className="badge badge-domain text-[10px]">{item.domain}</span>}
                      <span className="text-xs text-text-muted">{timeAgo(item.date_discovered)}</span>
                    </div>
                  </div>
                  <span className="text-xs text-text-muted font-mono">{relevance_score.toFixed(1)}</span>
                </div>
              </Link>
            ))}
            {data.results.length === 0 && (
              <div className="text-center py-12 text-text-muted">
                <SearchIcon className="w-8 h-8 mx-auto mb-3 opacity-50" />
                <p>No results found for "{data.query}"</p>
              </div>
            )}
          </div>

          {/* Facets Sidebar */}
          <div className="space-y-4">
            {Object.keys(data.facets.sources).length > 0 && (
              <div className="glow-card p-4">
                <h4 className="text-xs font-medium text-text-muted mb-3 uppercase tracking-wider">Sources</h4>
                {Object.entries(data.facets.sources).map(([label, count]) => (
                  <div key={label} className="flex items-center gap-2 py-1">
                    <div className={`w-2 h-2 rounded-full source-dot-${label}`} />
                    <span className="text-xs text-text-secondary flex-1">{sourceLabel(label)}</span>
                    <span className="text-xs text-text-muted font-mono">{count}</span>
                  </div>
                ))}
              </div>
            )}
            {Object.keys(data.facets.industries).length > 0 && (
              <div className="glow-card p-4">
                <h4 className="text-xs font-medium text-text-muted mb-3 uppercase tracking-wider">Industries</h4>
                {Object.entries(data.facets.industries).map(([label, count]) => (
                  <div key={label} className="flex items-center gap-2 py-1">
                    <span className="text-xs text-text-secondary flex-1">{label}</span>
                    <span className="text-xs text-text-muted font-mono">{count}</span>
                  </div>
                ))}
              </div>
            )}
            {Object.keys(data.facets.domains).length > 0 && (
              <div className="glow-card p-4">
                <h4 className="text-xs font-medium text-text-muted mb-3 uppercase tracking-wider">Domains</h4>
                {Object.entries(data.facets.domains).map(([label, count]) => (
                  <div key={label} className="flex items-center gap-2 py-1">
                    <span className="text-xs text-text-secondary flex-1">{label}</span>
                    <span className="text-xs text-text-muted font-mono">{count}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {!data && !loading && (
        <div className="text-center py-20 text-text-muted">
          <SearchIcon className="w-12 h-12 mx-auto mb-4 opacity-30" />
          <p className="text-lg">Search the research database</p>
          <p className="text-sm mt-1">Try "efficiency", "healthcare optimization", or "supply chain"</p>
        </div>
      )}

      {loading && (
        <div className="text-center py-20 text-text-muted">
          <div className="w-8 h-8 mx-auto border-2 border-accent-cyan/30 border-t-accent-cyan rounded-full animate-spin" />
          <p className="mt-4 text-sm">Searching...</p>
        </div>
      )}
    </div>
  );
}

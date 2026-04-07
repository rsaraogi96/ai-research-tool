import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { ChevronLeft, ChevronRight, ExternalLink, Grid3X3, List } from 'lucide-react';
import { apiGet, type ResearchInstance, type InstanceListResponse } from '@/api/client';
import { sourceLabel, sourceColor, timeAgo, truncate } from '@/lib/utils';

export default function Browse() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState<InstanceListResponse | null>(null);
  const [view, setView] = useState<'table' | 'cards'>('cards');

  const page = parseInt(searchParams.get('page') || '1');
  const sourceType = searchParams.get('source_type') || '';
  const industry = searchParams.get('industry') || '';
  const domain = searchParams.get('domain') || '';

  useEffect(() => {
    const params: Record<string, string | number> = { page, per_page: 20 };
    if (sourceType) params.source_type = sourceType;
    if (industry) params.industry = industry;
    if (domain) params.domain = domain;
    apiGet<InstanceListResponse>('/instances', params).then(setData);
  }, [page, sourceType, industry, domain]);

  const setFilter = (key: string, value: string) => {
    const p = new URLSearchParams(searchParams);
    if (value) p.set(key, value);
    else p.delete(key);
    p.set('page', '1');
    setSearchParams(p);
  };

  return (
    <div className="space-y-4">
      {/* Filters Bar */}
      <div className="flex items-center gap-3 flex-wrap">
        <h2 className="text-lg font-semibold text-text-primary mr-4">Browse Research</h2>

        <select
          value={sourceType}
          onChange={e => setFilter('source_type', e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-bg-card border border-border text-sm text-text-secondary focus:border-accent-blue/50 focus:outline-none"
        >
          <option value="">All Sources</option>
          <option value="arxiv">ArXiv</option>
          <option value="semantic_scholar">Semantic Scholar</option>
          <option value="rss">Blog Posts</option>
          <option value="manual">Manual</option>
        </select>

        <select
          value={industry}
          onChange={e => setFilter('industry', e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-bg-card border border-border text-sm text-text-secondary focus:border-accent-blue/50 focus:outline-none"
        >
          <option value="">All Industries</option>
          {['Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Energy', 'Transportation', 'Logistics', 'Education'].map(i => (
            <option key={i} value={i}>{i}</option>
          ))}
        </select>

        <select
          value={domain}
          onChange={e => setFilter('domain', e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-bg-card border border-border text-sm text-text-secondary focus:border-accent-blue/50 focus:outline-none"
        >
          <option value="">All Domains</option>
          {['Economics', 'Operations Research', 'Efficiency', 'Optimization', 'Forecasting', 'Supply Chain', 'Pricing', 'Automation'].map(d => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>

        <div className="flex-1" />

        <span className="text-xs text-text-muted">{data?.total ?? 0} results</span>

        <div className="flex border border-border rounded-lg overflow-hidden">
          <button onClick={() => setView('cards')} className={`p-1.5 ${view === 'cards' ? 'bg-accent-blue/20 text-accent-cyan' : 'text-text-muted hover:text-text-secondary'}`}>
            <Grid3X3 className="w-4 h-4" />
          </button>
          <button onClick={() => setView('table')} className={`p-1.5 ${view === 'table' ? 'bg-accent-blue/20 text-accent-cyan' : 'text-text-muted hover:text-text-secondary'}`}>
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Cards View */}
      {view === 'cards' && (
        <div className="grid grid-cols-2 gap-4">
          {data?.items.map(item => (
            <Link key={item.id} to={`/instance/${item.id}`} className="glow-card p-4 block group">
              <div className="flex items-start gap-3">
                <div className={`w-2.5 h-2.5 rounded-full mt-1 flex-shrink-0 source-dot-${item.source_type}`} />
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-text-primary group-hover:text-accent-cyan transition-colors line-clamp-2">
                    {item.title}
                  </h3>
                  {item.description && (
                    <p className="text-xs text-text-muted mt-1 line-clamp-2">{truncate(item.description, 150)}</p>
                  )}
                  <div className="flex items-center gap-2 mt-2 flex-wrap">
                    <span className={`text-xs font-medium source-${item.source_type}`}>{sourceLabel(item.source_type)}</span>
                    {item.company && <span className="text-xs text-text-secondary">{item.company.name}</span>}
                    {item.industry && <span className="badge badge-industry text-[10px]">{item.industry}</span>}
                    {item.domain && <span className="badge badge-domain text-[10px]">{item.domain}</span>}
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-xs text-text-muted">{timeAgo(item.date_discovered)}</span>
                    {item.source_url && (
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={e => e.stopPropagation()}
                        className="text-xs text-accent-blue hover:text-accent-cyan flex items-center gap-1"
                      >
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Table View */}
      {view === 'table' && (
        <div className="glow-card overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left p-3 text-text-muted font-medium text-xs">Source</th>
                <th className="text-left p-3 text-text-muted font-medium text-xs">Title</th>
                <th className="text-left p-3 text-text-muted font-medium text-xs">Company</th>
                <th className="text-left p-3 text-text-muted font-medium text-xs">Industry</th>
                <th className="text-left p-3 text-text-muted font-medium text-xs">Domain</th>
                <th className="text-left p-3 text-text-muted font-medium text-xs">Discovered</th>
              </tr>
            </thead>
            <tbody>
              {data?.items.map(item => (
                <tr key={item.id} className="border-b border-border/50 hover:bg-bg-hover transition-colors">
                  <td className="p-3">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full source-dot-${item.source_type}`} />
                      <span className={`text-xs source-${item.source_type}`}>{sourceLabel(item.source_type)}</span>
                    </div>
                  </td>
                  <td className="p-3">
                    <Link to={`/instance/${item.id}`} className="text-text-primary hover:text-accent-cyan transition-colors">
                      {truncate(item.title, 80)}
                    </Link>
                  </td>
                  <td className="p-3 text-text-secondary text-xs">{item.company?.name || '-'}</td>
                  <td className="p-3">{item.industry ? <span className="badge badge-industry text-[10px]">{item.industry}</span> : '-'}</td>
                  <td className="p-3">{item.domain ? <span className="badge badge-domain text-[10px]">{item.domain}</span> : '-'}</td>
                  <td className="p-3 text-text-muted text-xs">{timeAgo(item.date_discovered)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {data && data.total > 20 && (
        <div className="flex items-center justify-center gap-2">
          <button
            disabled={page <= 1}
            onClick={() => setFilter('page', String(page - 1))}
            className="p-2 rounded-lg border border-border text-text-muted hover:text-text-primary hover:border-accent-blue/50 disabled:opacity-30 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-sm text-text-secondary px-4">
            Page {page} of {Math.ceil(data.total / 20)}
          </span>
          <button
            disabled={page >= Math.ceil(data.total / 20)}
            onClick={() => setFilter('page', String(page + 1))}
            className="p-2 rounded-lg border border-border text-text-muted hover:text-text-primary hover:border-accent-blue/50 disabled:opacity-30 transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}

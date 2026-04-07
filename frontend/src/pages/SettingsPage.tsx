import { useEffect, useState } from 'react';
import { Play, RefreshCw, CheckCircle, XCircle, Clock } from 'lucide-react';
import { apiGet, apiPost, type CollectorStatus } from '@/api/client';
import { timeAgo } from '@/lib/utils';

export default function SettingsPage() {
  const [collectors, setCollectors] = useState<CollectorStatus[]>([]);
  const [running, setRunning] = useState<string | null>(null);
  const [result, setResult] = useState<{ name: string; found: number; added: number } | null>(null);

  const loadCollectors = () => {
    apiGet<CollectorStatus[]>('/collectors').then(setCollectors);
  };

  useEffect(loadCollectors, []);

  const runCollector = async (name: string) => {
    setRunning(name);
    setResult(null);
    try {
      const res = await apiPost<{ collector: string; items_found: number; items_added: number }>(`/collectors/${name}/run`);
      setResult({ name: res.collector, found: res.items_found, added: res.items_added });
      loadCollectors();
    } catch (e) {
      console.error(e);
    }
    setRunning(null);
  };

  const collectorInfo: Record<string, { label: string; description: string; color: string }> = {
    arxiv: { label: 'ArXiv', description: 'Research papers from arXiv.org (cs.AI, cs.LG, cs.CL)', color: 'text-accent-orange' },
    semantic_scholar: { label: 'Semantic Scholar', description: 'Academic papers via Semantic Scholar API', color: 'text-accent-blue' },
    rss: { label: 'Company Blogs', description: 'RSS feeds from AI company engineering blogs', color: 'text-accent-green' },
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <h2 className="text-lg font-semibold text-text-primary">Settings & Collectors</h2>

      {/* Collector Cards */}
      <div className="space-y-3">
        {collectors.map(collector => {
          const info = collectorInfo[collector.name] || { label: collector.name, description: '', color: 'text-text-primary' };
          const isRunning = running === collector.name;

          return (
            <div key={collector.name} className="glow-card p-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full source-dot-${collector.name}`} />
                  <div>
                    <h3 className={`text-sm font-medium ${info.color}`}>{info.label}</h3>
                    <p className="text-xs text-text-muted mt-0.5">{info.description}</p>
                  </div>
                </div>
                <button
                  onClick={() => runCollector(collector.name)}
                  disabled={isRunning}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-blue/20 border border-accent-blue/40 text-accent-cyan text-sm hover:bg-accent-blue/30 disabled:opacity-50 transition-all"
                >
                  {isRunning ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <Play className="w-4 h-4" />
                  )}
                  {isRunning ? 'Running...' : 'Run Now'}
                </button>
              </div>

              <div className="mt-3 pt-3 border-t border-border flex items-center gap-6 text-xs text-text-muted">
                <span className="flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5" />
                  {collector.last_run ? `Last run ${timeAgo(collector.last_run)}` : 'Never run'}
                </span>
                {collector.last_status && (
                  <span className="flex items-center gap-1.5">
                    {collector.last_status === 'success' ? (
                      <CheckCircle className="w-3.5 h-3.5 text-accent-green" />
                    ) : (
                      <XCircle className="w-3.5 h-3.5 text-accent-red" />
                    )}
                    {collector.last_status}
                  </span>
                )}
                <span>
                  {collector.items_collected} items collected
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Result Banner */}
      {result && (
        <div className="glow-card p-4 border-accent-green/30">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-accent-green" />
            <div>
              <p className="text-sm text-text-primary">
                <span className="font-medium">{collectorInfo[result.name]?.label}</span> collection complete
              </p>
              <p className="text-xs text-text-muted mt-0.5">
                Found {result.found} items, added {result.added} new
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Quick Tips */}
      <div className="glow-card p-5">
        <h3 className="text-sm font-medium text-text-secondary mb-3">Quick Tips</h3>
        <ul className="space-y-2 text-xs text-text-muted">
          <li>Collectors run automatically on a schedule when the server is running.</li>
          <li>ArXiv searches for applied AI papers in economics, operations, healthcare, and more.</li>
          <li>Semantic Scholar provides citation data and cross-references with ArXiv.</li>
          <li>Blog RSS feeds monitor 18+ AI company engineering blogs for new posts.</li>
          <li>Add API keys in <code className="px-1 py-0.5 rounded bg-bg-primary text-accent-cyan">.env</code> for higher rate limits.</li>
        </ul>
      </div>
    </div>
  );
}

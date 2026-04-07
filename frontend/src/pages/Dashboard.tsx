import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Zap, FileText, Building2, Users, Radio, ArrowRight, ExternalLink } from 'lucide-react';
import { apiGet, type AnalyticsOverview, type BreakdownItem, type TimelinePoint, type ResearchInstance } from '@/api/client';
import { sourceLabel, sourceColor, timeAgo, truncate } from '@/lib/utils';

const INDUSTRY_COLORS = [
  '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b',
  '#10b981', '#ef4444', '#f97316', '#14b8a6', '#a855f7',
];

export default function Dashboard() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [industries, setIndustries] = useState<BreakdownItem[]>([]);
  const [timeline, setTimeline] = useState<TimelinePoint[]>([]);
  const [recent, setRecent] = useState<ResearchInstance[]>([]);
  const [sources, setSources] = useState<BreakdownItem[]>([]);

  useEffect(() => {
    apiGet<AnalyticsOverview>('/analytics/overview').then(setOverview);
    apiGet<{ items: BreakdownItem[] }>('/analytics/industry').then(d => setIndustries(d.items));
    apiGet<{ points: TimelinePoint[] }>('/analytics/timeline', { granularity: 'week' }).then(d => setTimeline(d.points));
    apiGet<{ items: ResearchInstance[]; total: number }>('/instances', { per_page: 8, sort_by: 'date_discovered', sort_order: 'desc' }).then(d => setRecent(d.items));
    apiGet<{ items: BreakdownItem[] }>('/analytics/source').then(d => setSources(d.items));
  }, []);

  const stats = [
    { label: 'Total Instances', value: overview?.total_instances ?? 0, icon: FileText, color: 'text-accent-cyan' },
    { label: 'This Week', value: overview?.instances_this_week ?? 0, icon: Zap, color: 'text-accent-green' },
    { label: 'Companies', value: overview?.total_companies ?? 0, icon: Building2, color: 'text-accent-purple' },
    { label: 'Following', value: overview?.total_people_following ?? 0, icon: Users, color: 'text-accent-pink' },
    { label: 'Sources Active', value: overview?.sources_active ?? 0, icon: Radio, color: 'text-accent-orange' },
  ];

  return (
    <div className="space-y-6">
      {/* Stats Row */}
      <div className="grid grid-cols-5 gap-4">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="glow-card p-4">
            <div className="flex items-center justify-between mb-2">
              <Icon className={`w-5 h-5 ${color}`} />
              <span className="text-2xl font-bold text-text-primary">{value}</span>
            </div>
            <p className="text-xs text-text-muted">{label}</p>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-4">
        {/* Timeline */}
        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Discovery Timeline</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={timeline}>
              <defs>
                <linearGradient id="timelineGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#06b6d4" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3142', borderRadius: 8, color: '#e2e8f0' }}
              />
              <Area type="monotone" dataKey="count" stroke="#06b6d4" fill="url(#timelineGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Industry Breakdown */}
        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Industry Breakdown</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={industries.slice(0, 8)} layout="vertical">
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="label" tick={{ fill: '#94a3b8', fontSize: 11 }} width={100} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3142', borderRadius: 8, color: '#e2e8f0' }}
              />
              <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                {industries.slice(0, 8).map((_, i) => (
                  <Cell key={i} fill={INDUSTRY_COLORS[i % INDUSTRY_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Source breakdown + Recent */}
      <div className="grid grid-cols-3 gap-4">
        {/* Sources */}
        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">By Source</h3>
          <div className="space-y-3">
            {sources.map((s) => (
              <div key={s.label} className="flex items-center gap-3">
                <div className={`w-2.5 h-2.5 rounded-full source-dot-${s.label}`} />
                <span className="text-sm text-text-secondary flex-1">{sourceLabel(s.label)}</span>
                <span className="text-sm font-mono text-text-primary">{s.count}</span>
                <span className="text-xs text-text-muted w-12 text-right">{s.percentage}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Instances */}
        <div className="glow-card p-4 col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-text-secondary">Recent Discoveries</h3>
            <Link to="/browse" className="text-xs text-accent-cyan hover:text-accent-blue flex items-center gap-1 transition-colors">
              View all <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="space-y-2">
            {recent.map((item) => (
              <Link
                key={item.id}
                to={`/instance/${item.id}`}
                className="flex items-start gap-3 p-2 rounded-lg hover:bg-bg-hover transition-colors group"
              >
                <div className={`w-2 h-2 rounded-full mt-1.5 source-dot-${item.source_type}`} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-text-primary truncate group-hover:text-accent-cyan transition-colors">
                    {item.title}
                  </p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className={`text-xs source-${item.source_type}`}>{sourceLabel(item.source_type)}</span>
                    {item.company && <span className="text-xs text-text-muted">{item.company.name}</span>}
                    {item.industry && <span className="badge badge-industry text-[10px]">{item.industry}</span>}
                  </div>
                </div>
                <span className="text-xs text-text-muted whitespace-nowrap">{timeAgo(item.date_discovered)}</span>
              </Link>
            ))}
            {recent.length === 0 && (
              <p className="text-sm text-text-muted text-center py-8">
                No instances yet. Run a collector to get started!
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

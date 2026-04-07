import { useEffect, useState } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import { apiGet, type BreakdownItem, type TimelinePoint, type CompanyActivity as CA } from '@/api/client';

const COLORS = [
  '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b',
  '#10b981', '#ef4444', '#f97316', '#14b8a6', '#a855f7',
  '#6366f1', '#84cc16',
];

const tooltipStyle = { background: '#1a1f2e', border: '1px solid #2a3142', borderRadius: 8, color: '#e2e8f0' };

export default function Analytics() {
  const [industries, setIndustries] = useState<BreakdownItem[]>([]);
  const [domains, setDomains] = useState<BreakdownItem[]>([]);
  const [sources, setSources] = useState<BreakdownItem[]>([]);
  const [timeline, setTimeline] = useState<TimelinePoint[]>([]);
  const [companyActivity, setCompanyActivity] = useState<CA[]>([]);

  useEffect(() => {
    apiGet<{ items: BreakdownItem[] }>('/analytics/industry').then(d => setIndustries(d.items));
    apiGet<{ items: BreakdownItem[] }>('/analytics/domain').then(d => setDomains(d.items));
    apiGet<{ items: BreakdownItem[] }>('/analytics/source').then(d => setSources(d.items));
    apiGet<{ points: TimelinePoint[] }>('/analytics/timeline', { granularity: 'month' }).then(d => setTimeline(d.points));
    apiGet<{ items: CA[] }>('/analytics/companies').then(d => setCompanyActivity(d.items));
  }, []);

  // Transform company activity into pivoted data
  const companyMonths = Array.from(new Set(companyActivity.map(c => c.month))).sort();
  const topCompanies = Array.from(new Set(companyActivity.map(c => c.company))).slice(0, 8);
  const pivotedData = companyMonths.map(month => {
    const row: Record<string, string | number> = { month };
    topCompanies.forEach(comp => {
      const match = companyActivity.find(c => c.company === comp && c.month === month);
      row[comp] = match?.count || 0;
    });
    return row;
  });

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold text-text-primary">Analytics & Patterns</h2>

      {/* Row 1: Industry + Domain */}
      <div className="grid grid-cols-2 gap-4">
        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Industry Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={industries.slice(0, 10)} layout="vertical">
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="label" width={110} tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                {industries.slice(0, 10).map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Domain Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={domains.slice(0, 10)} layout="vertical">
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="label" width={130} tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                {domains.slice(0, 10).map((_, i) => (
                  <Cell key={i} fill={COLORS[(i + 3) % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 2: Timeline + Source Pie */}
      <div className="grid grid-cols-3 gap-4">
        <div className="glow-card p-4 col-span-2">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Monthly Discovery Timeline</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={timeline}>
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Line type="monotone" dataKey="count" stroke="#06b6d4" strokeWidth={2} dot={{ fill: '#06b6d4', r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Sources</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={sources} dataKey="count" nameKey="label" cx="50%" cy="50%" outerRadius={80} innerRadius={40} paddingAngle={2}>
                {sources.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} />
              <Legend
                formatter={(value: string) => <span className="text-xs text-text-secondary">{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 3: Company Activity Stacked */}
      {pivotedData.length > 0 && (
        <div className="glow-card p-4">
          <h3 className="text-sm font-medium text-text-secondary mb-4">Company Activity Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pivotedData}>
              <XAxis dataKey="month" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend
                formatter={(value: string) => <span className="text-xs text-text-secondary">{value}</span>}
              />
              {topCompanies.map((comp, i) => (
                <Bar key={comp} dataKey={comp} stackId="a" fill={COLORS[i % COLORS.length]} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

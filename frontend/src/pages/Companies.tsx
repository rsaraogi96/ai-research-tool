import { useEffect, useState } from 'react';
import { Building2, ExternalLink } from 'lucide-react';
import { apiGet, type Company } from '@/api/client';

export default function Companies() {
  const [companies, setCompanies] = useState<Company[]>([]);

  useEffect(() => {
    apiGet<{ items: Company[]; total: number }>('/companies', { per_page: 100 }).then(d => setCompanies(d.items));
  }, []);

  const sectorColor = (sector: string | null) => {
    switch (sector) {
      case 'big_tech': return 'text-accent-blue bg-accent-blue/15 border-accent-blue/30';
      case 'startup': return 'text-accent-green bg-accent-green/15 border-accent-green/30';
      case 'academic': return 'text-accent-purple bg-accent-purple/15 border-accent-purple/30';
      default: return 'text-text-muted bg-bg-primary border-border';
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-text-primary">Companies</h2>

      <div className="grid grid-cols-3 gap-4">
        {companies.map(company => (
          <div key={company.id} className="glow-card p-4">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
                  <Building2 className="w-5 h-5 text-accent-cyan" />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-text-primary">{company.name}</h3>
                  {company.sector && (
                    <span className={`inline-block text-[10px] px-1.5 py-0.5 rounded border mt-1 ${sectorColor(company.sector)}`}>
                      {company.sector.replace('_', ' ')}
                    </span>
                  )}
                </div>
              </div>
              {company.website && (
                <a href={company.website} target="_blank" rel="noopener noreferrer" className="text-text-muted hover:text-accent-cyan">
                  <ExternalLink className="w-4 h-4" />
                </a>
              )}
            </div>
            <div className="mt-3 pt-3 border-t border-border flex items-center justify-between">
              <span className="text-xs text-text-muted">Research instances</span>
              <span className="text-lg font-bold text-accent-cyan font-mono">{company.instance_count}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, ExternalLink, Calendar, Building2, Tag, User, Link as LinkIcon } from 'lucide-react';
import { apiGet, type ResearchInstance } from '@/api/client';
import { sourceLabel, timeAgo } from '@/lib/utils';

export default function InstancePage() {
  const { id } = useParams();
  const [instance, setInstance] = useState<ResearchInstance | null>(null);

  useEffect(() => {
    if (id) apiGet<ResearchInstance>(`/instances/${id}`).then(setInstance);
  }, [id]);

  if (!instance) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-accent-cyan/30 border-t-accent-cyan rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl space-y-6">
      {/* Back link */}
      <Link to="/browse" className="inline-flex items-center gap-2 text-sm text-text-muted hover:text-accent-cyan transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to browse
      </Link>

      {/* Header */}
      <div className="glow-card p-6">
        <div className="flex items-start gap-4">
          <div className={`w-3 h-3 rounded-full mt-1.5 source-dot-${instance.source_type}`} />
          <div className="flex-1">
            <h1 className="text-xl font-semibold text-text-primary leading-tight">{instance.title}</h1>
            <div className="flex items-center gap-3 mt-3 flex-wrap">
              <span className={`text-sm font-medium source-${instance.source_type}`}>
                {sourceLabel(instance.source_type)}
              </span>
              {instance.company && (
                <span className="flex items-center gap-1 text-sm text-text-secondary">
                  <Building2 className="w-3.5 h-3.5" /> {instance.company.name}
                </span>
              )}
              {instance.date_published && (
                <span className="flex items-center gap-1 text-sm text-text-muted">
                  <Calendar className="w-3.5 h-3.5" /> {instance.date_published}
                </span>
              )}
              <span className="text-xs text-text-muted">Discovered {timeAgo(instance.date_discovered)}</span>
            </div>
          </div>
          {instance.source_url && (
            <a
              href={instance.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-1.5 rounded-lg bg-accent-blue/20 border border-accent-blue/40 text-accent-cyan text-sm flex items-center gap-1.5 hover:bg-accent-blue/30 transition-all"
            >
              <ExternalLink className="w-3.5 h-3.5" /> Open Source
            </a>
          )}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Main Content */}
        <div className="col-span-2 space-y-4">
          {/* Description */}
          {instance.description && (
            <div className="glow-card p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-3">Description</h3>
              <p className="text-sm text-text-primary leading-relaxed whitespace-pre-wrap">
                {instance.description}
              </p>
            </div>
          )}

          {/* Links */}
          {instance.links.length > 0 && (
            <div className="glow-card p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-3 flex items-center gap-2">
                <LinkIcon className="w-4 h-4" /> Links
              </h3>
              <div className="space-y-2">
                {instance.links.map(link => (
                  <a
                    key={link.id}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-bg-hover transition-colors group"
                  >
                    <ExternalLink className="w-4 h-4 text-accent-blue group-hover:text-accent-cyan" />
                    <span className="text-sm text-text-primary group-hover:text-accent-cyan transition-colors">
                      {link.title || link.url}
                    </span>
                    {link.link_type && (
                      <span className="text-xs text-text-muted px-2 py-0.5 rounded bg-bg-primary">
                        {link.link_type}
                      </span>
                    )}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Metadata */}
          <div className="glow-card p-5">
            <h3 className="text-sm font-medium text-text-secondary mb-3">Details</h3>
            <dl className="space-y-3 text-sm">
              {instance.industry && (
                <div>
                  <dt className="text-text-muted text-xs">Industry</dt>
                  <dd className="mt-0.5"><span className="badge badge-industry">{instance.industry}</span></dd>
                </div>
              )}
              {instance.domain && (
                <div>
                  <dt className="text-text-muted text-xs">Domain</dt>
                  <dd className="mt-0.5"><span className="badge badge-domain">{instance.domain}</span></dd>
                </div>
              )}
              <div>
                <dt className="text-text-muted text-xs">Source ID</dt>
                <dd className="mt-0.5 text-text-secondary font-mono text-xs">{instance.source_id || '-'}</dd>
              </div>
              <div>
                <dt className="text-text-muted text-xs">Relevance Score</dt>
                <dd className="mt-0.5 text-text-secondary">{instance.relevance_score.toFixed(1)}</dd>
              </div>
              <div>
                <dt className="text-text-muted text-xs">Curated</dt>
                <dd className="mt-0.5">{instance.is_curated ? '✓ Yes' : 'No'}</dd>
              </div>
            </dl>
          </div>

          {/* Tags */}
          {instance.tags.length > 0 && (
            <div className="glow-card p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-3 flex items-center gap-2">
                <Tag className="w-4 h-4" /> Tags
              </h3>
              <div className="flex flex-wrap gap-1.5">
                {instance.tags.map(tag => (
                  <span key={tag.id} className={`badge badge-${tag.category || 'method'}`}>
                    {tag.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* People */}
          {instance.people.length > 0 && (
            <div className="glow-card p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-3 flex items-center gap-2">
                <User className="w-4 h-4" /> People
              </h3>
              <div className="space-y-2">
                {instance.people.map(person => (
                  <div key={person.id} className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-accent-purple/20 flex items-center justify-center text-xs text-accent-purple">
                      {person.name[0]}
                    </div>
                    <div>
                      <p className="text-xs text-text-primary">{person.name}</p>
                      {person.affiliation && <p className="text-[10px] text-text-muted">{person.affiliation}</p>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

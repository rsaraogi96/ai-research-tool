import { useEffect, useState } from 'react';
import { UserPlus, Star, StarOff } from 'lucide-react';
import { apiGet, apiPatch, type Person } from '@/api/client';

export default function People() {
  const [people, setPeople] = useState<Person[]>([]);
  const [total, setTotal] = useState(0);
  const [followingOnly, setFollowingOnly] = useState(false);

  const loadPeople = () => {
    apiGet<{ items: Person[]; total: number }>('/people', { following_only: followingOnly, per_page: 100 })
      .then(d => { setPeople(d.items); setTotal(d.total); });
  };

  useEffect(loadPeople, [followingOnly]);

  const toggleFollow = async (id: number) => {
    await apiPatch(`/people/${id}/follow`);
    loadPeople();
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-text-primary">People</h2>
        <button
          onClick={() => setFollowingOnly(!followingOnly)}
          className={`px-3 py-1.5 rounded-lg text-xs border transition-all ${
            followingOnly
              ? 'bg-accent-pink/20 border-accent-pink/40 text-accent-pink'
              : 'bg-bg-card border-border text-text-muted hover:text-text-secondary'
          }`}
        >
          {followingOnly ? 'Following' : 'All People'}
        </button>
        <span className="text-xs text-text-muted">{total} people</span>
      </div>

      <div className="glow-card overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left p-3 text-text-muted font-medium text-xs">Name</th>
              <th className="text-left p-3 text-text-muted font-medium text-xs">Affiliation</th>
              <th className="text-left p-3 text-text-muted font-medium text-xs">Instances</th>
              <th className="text-left p-3 text-text-muted font-medium text-xs">Website</th>
              <th className="text-center p-3 text-text-muted font-medium text-xs">Follow</th>
            </tr>
          </thead>
          <tbody>
            {people.map(person => (
              <tr key={person.id} className="border-b border-border/50 hover:bg-bg-hover transition-colors">
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full bg-accent-purple/20 flex items-center justify-center text-xs text-accent-purple font-medium">
                      {person.name[0]}
                    </div>
                    <span className="text-text-primary">{person.name}</span>
                  </div>
                </td>
                <td className="p-3 text-text-secondary text-xs">{person.affiliation || '-'}</td>
                <td className="p-3">
                  <span className="text-xs font-mono text-accent-cyan">{person.instance_count}</span>
                </td>
                <td className="p-3">
                  {person.website ? (
                    <a href={person.website} target="_blank" rel="noopener noreferrer" className="text-xs text-accent-blue hover:text-accent-cyan">
                      Link
                    </a>
                  ) : '-'}
                </td>
                <td className="p-3 text-center">
                  <button
                    onClick={() => toggleFollow(person.id)}
                    className={`p-1.5 rounded-lg transition-all ${
                      person.is_following
                        ? 'text-accent-pink hover:text-accent-pink/70'
                        : 'text-text-muted hover:text-accent-pink'
                    }`}
                  >
                    {person.is_following ? <Star className="w-4 h-4 fill-current" /> : <StarOff className="w-4 h-4" />}
                  </button>
                </td>
              </tr>
            ))}
            {people.length === 0 && (
              <tr>
                <td colSpan={5} className="p-8 text-center text-text-muted">
                  No people found. Run collectors to discover researchers.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

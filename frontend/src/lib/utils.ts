import { formatDistanceToNow, parseISO } from 'date-fns';

export function cn(...classes: (string | undefined | false | null)[]): string {
  return classes.filter(Boolean).join(' ');
}

export function sourceLabel(type: string): string {
  const labels: Record<string, string> = {
    arxiv: 'ArXiv',
    semantic_scholar: 'Semantic Scholar',
    rss: 'Blog',
    manual: 'Manual',
  };
  return labels[type] || type;
}

export function sourceColor(type: string): string {
  const colors: Record<string, string> = {
    arxiv: '#f59e0b',
    semantic_scholar: '#3b82f6',
    rss: '#10b981',
    manual: '#8b5cf6',
  };
  return colors[type] || '#64748b';
}

export function timeAgo(dateStr: string | null): string {
  if (!dateStr) return 'Unknown';
  try {
    return formatDistanceToNow(parseISO(dateStr), { addSuffix: true });
  } catch {
    return dateStr;
  }
}

export function truncate(str: string, len: number): string {
  if (str.length <= len) return str;
  return str.slice(0, len) + '...';
}

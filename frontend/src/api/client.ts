const API_BASE = '/api/v1';

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export async function apiGet<T>(path: string, params?: Record<string, string | number | boolean | undefined>): Promise<T> {
  const url = new URL(`${window.location.origin}${API_BASE}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        url.searchParams.set(k, String(v));
      }
    });
  }
  const res = await fetch(url.toString());
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json();
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json();
}

export async function apiPut<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json();
}

export async function apiPatch<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json();
}

export async function apiDelete(path: string): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, { method: 'DELETE' });
  if (!res.ok) throw new ApiError(res.status, await res.text());
}

// Types
export interface ResearchInstance {
  id: number;
  title: string;
  description: string | null;
  source_type: string;
  source_id: string | null;
  source_url: string | null;
  company: { id: number; name: string; sector: string | null } | null;
  industry: string | null;
  domain: string | null;
  date_published: string | null;
  date_discovered: string | null;
  relevance_score: number;
  is_curated: boolean;
  tags: { id: number; name: string; category: string | null }[];
  people: { id: number; name: string; affiliation: string | null; is_following: boolean }[];
  links: { id: number; url: string; link_type: string | null; title: string | null }[];
  created_at: string | null;
}

export interface InstanceListResponse {
  items: ResearchInstance[];
  total: number;
  page: number;
  per_page: number;
}

export interface SearchResult {
  instance: ResearchInstance;
  relevance_score: number;
  title_snippet: string | null;
  description_snippet: string | null;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  page: number;
  per_page: number;
  query: string;
  facets: {
    sources: Record<string, number>;
    industries: Record<string, number>;
    domains: Record<string, number>;
  };
}

export interface AnalyticsOverview {
  total_instances: number;
  instances_this_week: number;
  total_companies: number;
  total_people_following: number;
  sources_active: number;
}

export interface BreakdownItem {
  label: string;
  count: number;
  percentage: number;
}

export interface TimelinePoint {
  date: string;
  count: number;
}

export interface CompanyActivity {
  company: string;
  month: string;
  count: number;
}

export interface Company {
  id: number;
  name: string;
  website: string | null;
  sector: string | null;
  description: string | null;
  instance_count: number;
}

export interface Person {
  id: number;
  name: string;
  email: string | null;
  affiliation: string | null;
  website: string | null;
  notes: string | null;
  is_following: boolean;
  instance_count: number;
}

export interface CollectorStatus {
  name: string;
  last_run: string | null;
  last_status: string | null;
  items_collected: number;
}

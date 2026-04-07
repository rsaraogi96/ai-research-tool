import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  List,
  Search,
  Users,
  Building2,
  BarChart3,
  Settings,
  Zap,
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/browse', icon: List, label: 'Browse' },
  { to: '/search', icon: Search, label: 'Search' },
  { to: '/people', icon: Users, label: 'People' },
  { to: '/companies', icon: Building2, label: 'Companies' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  return (
    <aside className="w-56 flex-shrink-0 border-r border-border bg-bg-secondary flex flex-col h-screen sticky top-0">
      {/* Logo */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent-blue/20 flex items-center justify-center">
            <Zap className="w-5 h-5 text-accent-cyan" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-text-primary tracking-tight">AI Research</h1>
            <p className="text-xs text-text-muted">Tracker</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200 ${
                isActive
                  ? 'bg-accent-blue/15 text-accent-cyan border border-accent-blue/30 shadow-[0_0_10px_rgba(6,182,212,0.15)]'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-hover'
              }`
            }
          >
            <Icon className="w-4 h-4" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Status indicator */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-2 text-xs text-text-muted">
          <div className="w-2 h-2 rounded-full bg-accent-green pulse-dot" />
          <span>Live tracking</span>
        </div>
      </div>
    </aside>
  );
}

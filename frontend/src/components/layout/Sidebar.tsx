import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Users, FolderOpen, Megaphone,
  FileText, Bot, BarChart3, Settings, Target, Package, TrendingUp,
} from 'lucide-react';

const links = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/clients', icon: Users, label: 'Clientes' },
  { to: '/projects', icon: FolderOpen, label: 'Proyectos' },
  { to: '/campaigns', icon: Megaphone, label: 'Campanas' },
  { to: '/content', icon: FileText, label: 'Contenido' },
  { to: '/agents', icon: Bot, label: 'Agentes IA' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { divider: true },
  { to: '/potenciales', icon: Target, label: 'Potenciales' },
  { to: '/produccion', icon: Package, label: 'Producción' },
  { to: '/dashboards', icon: TrendingUp, label: 'Dashboards' },
  { divider: true },
  { to: '/settings', icon: Settings, label: 'Config' },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-primary-700">AI Marketing</h1>
        <p className="text-xs text-gray-500 mt-1">Agency Platform</p>
      </div>
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {links.map((link, idx) => {
          if ('divider' in link && link.divider) {
            return <div key={idx} className="my-2 border-t border-gray-200" />;
          }
          const { to, icon: Icon, label } = link as any;
          return (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <div className="w-2 h-2 rounded-full bg-green-400" />
          Sistema activo
        </div>
      </div>
    </aside>
  );
}

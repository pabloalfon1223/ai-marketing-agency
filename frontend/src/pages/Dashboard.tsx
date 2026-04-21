import { useQuery } from '@tanstack/react-query';
import { Users, FolderOpen, Megaphone, FileText, Bot, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import Header from '../components/layout/Header';
import StatusBadge from '../components/shared/StatusBadge';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import { getAnalyticsOverview } from '../api/agents';
import { getAgentsStatus } from '../api/agents';
import { getTasks } from '../api/agents';
import { formatDateTime, agentDisplayNames } from '../utils/formatters';

export default function Dashboard() {
  const { data: overview, isLoading } = useQuery({ queryKey: ['analytics', 'overview'], queryFn: getAnalyticsOverview });
  const { data: agents } = useQuery({ queryKey: ['agents-status'], queryFn: getAgentsStatus });
  const { data: recentTasks } = useQuery({ queryKey: ['tasks', 'recent'], queryFn: () => getTasks({ status: 'running' }) });

  if (isLoading) return <><Header title="Dashboard" /><LoadingSpinner /></>;

  const stats = [
    { label: 'Clientes', value: overview?.total_clients ?? 0, icon: Users, color: 'bg-blue-500' },
    { label: 'Proyectos', value: overview?.total_projects ?? 0, icon: FolderOpen, color: 'bg-green-500' },
    { label: 'Campanas', value: overview?.total_campaigns ?? 0, icon: Megaphone, color: 'bg-purple-500' },
    { label: 'Contenido', value: overview?.total_content ?? 0, icon: FileText, color: 'bg-orange-500' },
  ];

  return (
    <>
      <Header title="Dashboard" />
      <div className="p-6 space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="bg-white rounded-xl border border-gray-200 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">{label}</p>
                  <p className="text-2xl font-bold mt-1">{value}</p>
                </div>
                <div className={`${color} p-3 rounded-lg`}>
                  <Icon size={20} className="text-white" />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Agent Status */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Bot size={16} /> Estado de Agentes
            </h3>
            <div className="space-y-3">
              {agents?.length ? agents.map((agent: any) => (
                <div key={agent.agent_type} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${agent.tasks_running > 0 ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`} />
                    <span className="text-sm font-medium">{agent.display_name}</span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    <span className="flex items-center gap-1"><CheckCircle size={12} /> {agent.tasks_completed}</span>
                    {agent.tasks_running > 0 && (
                      <span className="flex items-center gap-1 text-yellow-600"><Clock size={12} /> {agent.tasks_running}</span>
                    )}
                  </div>
                </div>
              )) : (
                <p className="text-sm text-gray-400">Sin agentes registrados. Lanza tu primera tarea.</p>
              )}
            </div>
          </div>

          {/* Tasks & Activity */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Clock size={16} /> Tareas en Progreso
            </h3>
            <div className="space-y-3">
              {recentTasks?.length ? recentTasks.map((task: any) => (
                <div key={task.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                  <div>
                    <p className="text-sm font-medium">{agentDisplayNames[task.agent_type] || task.agent_type}</p>
                    <p className="text-xs text-gray-500">{task.task_type}</p>
                  </div>
                  <StatusBadge status={task.status} />
                </div>
              )) : (
                <p className="text-sm text-gray-400">No hay tareas en ejecucion.</p>
              )}
            </div>
          </div>
        </div>

        {/* Tasks by Status */}
        {overview?.tasks_by_status && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Resumen de Tareas</h3>
            <div className="flex gap-6">
              {Object.entries(overview.tasks_by_status).map(([status, count]) => (
                <div key={status} className="text-center">
                  <p className="text-2xl font-bold">{count as number}</p>
                  <StatusBadge status={status} />
                </div>
              ))}
              {Object.keys(overview.tasks_by_status).length === 0 && (
                <p className="text-sm text-gray-400">Sin tareas todavia.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
}

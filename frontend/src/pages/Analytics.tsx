import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import Header from '../components/layout/Header';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import { getAnalyticsOverview, getAgentAnalytics } from '../api/agents';

const COLORS = ['#4c6ef5', '#51cf66', '#fcc419', '#ff6b6b', '#845ef7', '#22b8cf', '#ff922b', '#20c997', '#e64980'];

export default function Analytics() {
  const { data: overview, isLoading } = useQuery({ queryKey: ['analytics', 'overview'], queryFn: getAnalyticsOverview });
  const { data: agentStats } = useQuery({ queryKey: ['analytics', 'agents'], queryFn: getAgentAnalytics });

  if (isLoading) return <><Header title="Analytics" /><LoadingSpinner /></>;

  const taskData = overview?.tasks_by_status
    ? Object.entries(overview.tasks_by_status).map(([name, value]) => ({ name, value }))
    : [];

  const contentData = overview?.content_by_status
    ? Object.entries(overview.content_by_status).map(([name, value]) => ({ name, value }))
    : [];

  const agentData = agentStats?.map((a: any) => ({
    name: a.agent_type,
    completed: a.tasks_completed,
    failed: a.tasks_failed,
    rate: a.success_rate,
  })) || [];

  return (
    <>
      <Header title="Analytics" />
      <div className="p-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl border border-gray-200 p-5 text-center">
            <p className="text-3xl font-bold text-primary-600">{overview?.total_clients ?? 0}</p>
            <p className="text-sm text-gray-500 mt-1">Clientes</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5 text-center">
            <p className="text-3xl font-bold text-green-600">{overview?.total_campaigns ?? 0}</p>
            <p className="text-sm text-gray-500 mt-1">Campanas</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5 text-center">
            <p className="text-3xl font-bold text-purple-600">{overview?.total_content ?? 0}</p>
            <p className="text-sm text-gray-500 mt-1">Contenido</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5 text-center">
            <p className="text-3xl font-bold text-orange-600">
              {taskData.reduce((acc, d) => acc + (d.value as number), 0)}
            </p>
            <p className="text-sm text-gray-500 mt-1">Tareas Total</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Tasks by Status */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Tareas por Estado</h3>
            {taskData.length ? (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={taskData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {taskData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 text-center py-8">Sin datos todavia</p>}
          </div>

          {/* Content by Status */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Contenido por Estado</h3>
            {contentData.length ? (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={contentData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {contentData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 text-center py-8">Sin datos todavia</p>}
          </div>
        </div>

        {/* Agent Performance */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Rendimiento por Agente</h3>
          {agentData.length ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={agentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="completed" name="Completadas" fill="#4c6ef5" radius={[4, 4, 0, 0]} />
                <Bar dataKey="failed" name="Fallidas" fill="#ff6b6b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-sm text-gray-400 text-center py-8">Sin datos todavia</p>}
        </div>
      </div>
    </>
  );
}

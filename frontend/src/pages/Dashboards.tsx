import { useQuery } from '@tanstack/react-query';
import { dashboardsAPI } from '../api/dashboards';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { Loader2, Target, TrendingUp, AlertTriangle, Package } from 'lucide-react';

const COLORS = ['#f59e0b', '#3b82f6', '#f97316', '#ef4444', '#8b5cf6', '#06b6d4', '#6366f1', '#10b981'];
const PRIORIDAD_COLORS = {
  'ALTA': '#ef4444',
  'MEDIA': '#eab308',
  'BAJA': '#22c55e',
};

export default function Dashboards() {
  // Fetch potenciales summary
  const { data: potencialesResumen = {} } = useQuery({
    queryKey: ['dashboards-potenciales-resumen'],
    queryFn: async () => {
      const res = await fetch('/api/v1/dashboards/potenciales/resumen');
      return res.json();
    },
    refetchInterval: 30000,
  });

  // Fetch funnel
  const { data: funnel = {} } = useQuery({
    queryKey: ['dashboards-funnel'],
    queryFn: async () => {
      const res = await fetch('/api/v1/dashboards/potenciales/funnel');
      return res.json();
    },
    refetchInterval: 30000,
  });

  // Fetch prioridad distribution
  const { data: prioridadData = {} } = useQuery({
    queryKey: ['dashboards-prioridad'],
    queryFn: async () => {
      const res = await fetch('/api/v1/dashboards/potenciales/por-prioridad');
      return res.json();
    },
    refetchInterval: 30000,
  });

  // Fetch producción summary
  const { data: produccionResumen = {} } = useQuery({
    queryKey: ['dashboards-produccion-resumen'],
    queryFn: async () => {
      const res = await fetch('/api/v1/dashboards/produccion/resumen');
      return res.json();
    },
    refetchInterval: 30000,
  });

  // Prepare chart data
  const funnelData = funnel && funnel.SIN_RESPUESTA !== undefined ? [
    { name: 'Sin Respuesta', count: funnel.SIN_RESPUESTA || 0 },
    { name: 'Esperamos Respuesta', count: funnel.ESPERAMOS_RESPUESTA || 0 },
    { name: 'Cotización Enviada', count: funnel.COTIZACION_ENVIADA || 0 },
    { name: 'Cliente', count: funnel.CLIENTE || 0 },
  ] : [];

  const prioridadChartData = prioridadData && prioridadData.ALTA !== undefined ? [
    { name: 'ALTA', value: prioridadData.ALTA || 0 },
    { name: 'MEDIA', value: prioridadData.MEDIA || 0 },
    { name: 'BAJA', value: prioridadData.BAJA || 0 },
  ] : [];

  const totalPotenciales = potencialesResumen?.total || 0;
  const clientesConvertidos = funnel?.CLIENTE || 0;
  const conversionRate = totalPotenciales > 0 ? ((clientesConvertidos / totalPotenciales) * 100).toFixed(1) : 0;

  if (!potencialesResumen || !produccionResumen) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6 p-4 md:p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboards</h1>
        <p className="text-gray-600 mt-2">Análisis consolidado de potenciales y producción</p>
      </div>

      {/* Main KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Potenciales</CardTitle>
            <Target className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{totalPotenciales}</div>
            <p className="text-xs text-gray-600 mt-2">En pipeline</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tasa Conversión</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{conversionRate}%</div>
            <p className="text-xs text-gray-600 mt-2">Convertidos a Cliente</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Producción</CardTitle>
            <Package className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{produccionResumen?.total || 0}</div>
            <p className="text-xs text-gray-600 mt-2">Órdenes activas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Alertas</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{produccionResumen?.alertas_sin_actualizar || 0}</div>
            <p className="text-xs text-gray-600 mt-2">Sin actualizar >5 días</p>
          </CardContent>
        </Card>
      </div>

      {/* Funnel and Prioridad Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Funnel Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Funnel de Conversión</CardTitle>
            <CardDescription>Potenciales por estado</CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            {funnelData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={funnelData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                Sin datos disponibles
              </div>
            )}
          </CardContent>
        </Card>

        {/* Prioridad Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Distribución por Prioridad</CardTitle>
            <CardDescription>Potenciales actuales</CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            {prioridadChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={prioridadChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {prioridadChartData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={PRIORIDAD_COLORS[entry.name as keyof typeof PRIORIDAD_COLORS] || '#8884d8'}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                Sin datos disponibles
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Estado Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Desglose por Estado</CardTitle>
          <CardDescription>Potenciales actuales en cada etapa</CardDescription>
        </CardHeader>
        <CardContent className="pt-4">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div className="space-y-2 p-3 bg-gray-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Sin Respuesta</p>
              <p className="text-2xl font-bold text-gray-700">
                {potencialesResumen.SIN_RESPUESTA || 0}
              </p>
            </div>

            <div className="space-y-2 p-3 bg-orange-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Esperamos</p>
              <p className="text-2xl font-bold text-orange-700">
                {potencialesResumen.ESPERAMOS_RESPUESTA || 0}
              </p>
            </div>

            <div className="space-y-2 p-3 bg-blue-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Cotización</p>
              <p className="text-2xl font-bold text-blue-700">
                {potencialesResumen.COTIZACION_ENVIADA || 0}
              </p>
            </div>

            <div className="space-y-2 p-3 bg-green-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Clientes ✅</p>
              <p className="text-2xl font-bold text-green-700">
                {potencialesResumen.CLIENTE || 0}
              </p>
            </div>

            <div className="space-y-2 p-3 bg-red-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Cerrar</p>
              <p className="text-2xl font-bold text-red-700">
                {potencialesResumen.CERRAR || 0}
              </p>
            </div>

            <div className="space-y-2 p-3 bg-red-50 rounded-lg text-center">
              <p className="text-xs text-gray-600">Recontactar</p>
              <p className="text-2xl font-bold text-red-700">
                {potencialesResumen.RECONTACTAR || 0}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Producción Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Resumen de Producción</CardTitle>
          <CardDescription>Estado de órdenes activas</CardDescription>
        </CardHeader>
        <CardContent className="pt-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <div className="space-y-2 p-4 bg-orange-50 rounded-lg">
              <p className="text-sm text-gray-600">Total Órdenes</p>
              <p className="text-2xl font-bold text-orange-700">
                {produccionResumen.total || 0}
              </p>
            </div>

            <div className="space-y-2 p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600">Finalizadas</p>
              <p className="text-2xl font-bold text-green-700">
                {produccionResumen.finalizados || 0}
              </p>
            </div>

            <div className="space-y-2 p-4 bg-red-50 rounded-lg">
              <p className="text-sm text-gray-600">Alertas >5 días</p>
              <p className="text-2xl font-bold text-red-700">
                {produccionResumen.alertas_sin_actualizar || 0}
              </p>
            </div>

            <div className="space-y-2 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600">Tasa Finalización</p>
              <p className="text-2xl font-bold text-blue-700">
                {produccionResumen.total > 0
                  ? ((produccionResumen.finalizados / produccionResumen.total) * 100).toFixed(0)
                  : 0}%
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

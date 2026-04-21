import { useQuery } from '@tanstack/react-query';
import { dashboardsAPI } from '../api/dashboards';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { Loader2, Target, TrendingUp, DollarSign, Package } from 'lucide-react';

const COLORS = ['#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'];
const ESTADO_COLORS = {
  'SIN_RESPUESTA': '#9ca3af',
  'ESPERAMOS_RESPUESTA': '#3b82f6',
  'COTIZACION_ENVIADA': '#f59e0b',
  'QUOTE_ACCEPTED': '#10b981',
  'ACCEPTED': '#3b82f6',
  'IN_PRODUCTION': '#f59e0b',
  'COMPLETED': '#8b5cf6',
  'DELIVERED': '#10b981',
};

export default function Dashboards() {
  // Fetch all dashboard data
  const { data: summary } = useQuery({
    queryKey: ['dashboards-summary'],
    queryFn: () => dashboardsAPI.summary(),
    refetchInterval: 30000,
  });

  const { data: funnel = {} } = useQuery({
    queryKey: ['dashboards-funnel'],
    queryFn: () => dashboardsAPI.funnelPotenciales(),
    refetchInterval: 30000,
  });

  const { data: valueByStatus = {} } = useQuery({
    queryKey: ['dashboards-value-by-status'],
    queryFn: () => dashboardsAPI.valueByStatus(),
    refetchInterval: 30000,
  });

  const { data: timeline = [] } = useQuery({
    queryKey: ['dashboards-timeline'],
    queryFn: () => dashboardsAPI.timelineProduccion(),
    refetchInterval: 30000,
  });

  // Prepare chart data
  const funnelData = Object.entries(funnel).map(([key, value]) => ({
    name: key.replace(/_/g, ' '),
    count: value as number,
  }));

  const valueData = Object.entries(valueByStatus).map(([key, value]) => ({
    name: key.replace(/_/g, ' '),
    value: value as number,
  }));

  const timelineChartData = timeline.slice(0, 10).map(item => ({
    ordenId: item.orden_id,
    cliente: item.cliente,
    inicio: new Date(item.fecha_inicio).getTime(),
    entrega: item.fecha_entrega_est ? new Date(item.fecha_entrega_est).getTime() : null,
    dias: item.dias_produccion || 0,
  }));

  if (!summary) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboards</h1>
        <p className="text-gray-600 mt-2">Análisis consolidado de potenciales y producción</p>
      </div>

      {/* Main KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Potenciales</CardTitle>
            <Target className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{summary.total_potenciales}</div>
            <p className="text-xs text-gray-600 mt-2">En pipeline</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{summary.conversion_rate.toFixed(1)}%</div>
            <p className="text-xs text-gray-600 mt-2">Potencial a Producción</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Valor Total Estimado</CardTitle>
            <DollarSign className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              ARS {(summary.total_estimated_value / 1000).toFixed(0)}k
            </div>
            <p className="text-xs text-gray-600 mt-2">En potenciales</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ingresos Realizados</CardTitle>
            <Package className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              ARS {(summary.total_ingresos / 1000).toFixed(0)}k
            </div>
            <p className="text-xs text-gray-600 mt-2">Órdenes entregadas</p>
          </CardContent>
        </Card>
      </div>

      {/* Funnel and Value Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Funnel Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Funnel de Conversión</CardTitle>
            <CardDescription>Potenciales por estado</CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={funnelData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Value by Status */}
        <Card>
          <CardHeader>
            <CardTitle>Valor Estimado por Estado</CardTitle>
            <CardDescription>Distribución de valor en potenciales</CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={valueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip formatter={(value) => `ARS ${value.toLocaleString('es-AR')}`} />
                <Bar dataKey="value" fill="#f59e0b" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Timeline and Production Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Production Timeline */}
        <Card>
          <CardHeader>
            <CardTitle>Timeline de Producción</CardTitle>
            <CardDescription>Próximas {Math.min(10, timeline.length)} entregas</CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            {timelineChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={timelineChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="ordenId" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip
                    formatter={(value) => `${value} días`}
                    labelFormatter={(label) => `Orden: ${label}`}
                  />
                  <Bar dataKey="dias" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                No hay datos de timeline disponibles
              </div>
            )}
          </CardContent>
        </Card>

        {/* Summary Stats */}
        <Card>
          <CardHeader>
            <CardTitle>Resumen Operacional</CardTitle>
            <CardDescription>Métricas clave del negocio</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 pt-4">
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-3 border-b">
                <span className="text-gray-600">Total Órdenes en Producción</span>
                <Badge variant="secondary">{summary.total_produccion}</Badge>
              </div>

              <div className="flex justify-between items-center pb-3 border-b">
                <span className="text-gray-600">Tasa de Conversión</span>
                <Badge className="bg-green-100 text-green-800">
                  {summary.conversion_rate.toFixed(1)}%
                </Badge>
              </div>

              <div className="flex justify-between items-center pb-3 border-b">
                <span className="text-gray-600">Valor Promedio Potencial</span>
                <span className="font-semibold">
                  ARS {summary.total_potenciales > 0
                    ? (summary.total_estimated_value / summary.total_potenciales).toLocaleString(
                        'es-AR',
                        { maximumFractionDigits: 0 }
                      )
                    : 0}
                </span>
              </div>

              <div className="flex justify-between items-center pb-3 border-b">
                <span className="text-gray-600">Valor Promedio Orden</span>
                <span className="font-semibold">
                  ARS {summary.total_produccion > 0
                    ? (summary.total_ingresos / summary.total_produccion).toLocaleString('es-AR', {
                        maximumFractionDigits: 0,
                      })
                    : 0}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-600">Margen Operacional (Est.)</span>
                <Badge variant="outline">Pendiente</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Trends */}
      <Card>
        <CardHeader>
          <CardTitle>Análisis de Desempeño</CardTitle>
          <CardDescription>Evolución de métricas clave</CardDescription>
        </CardHeader>
        <CardContent className="pt-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="space-y-2 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600">Potenciales Sin Respuesta</p>
              <p className="text-2xl font-bold text-blue-600">
                {Object.entries(funnel).find(([k]) => k === 'SIN_RESPUESTA')?.[1] || 0}
              </p>
              <p className="text-xs text-gray-500">Requiere seguimiento</p>
            </div>

            <div className="space-y-2 p-4 bg-orange-50 rounded-lg">
              <p className="text-sm text-gray-600">En Cotización</p>
              <p className="text-2xl font-bold text-orange-600">
                {Object.entries(funnel).find(([k]) => k === 'COTIZACION_ENVIADA')?.[1] || 0}
              </p>
              <p className="text-xs text-gray-500">Esperando decisión</p>
            </div>

            <div className="space-y-2 p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600">Aceptadas</p>
              <p className="text-2xl font-bold text-green-600">
                {Object.entries(funnel).find(([k]) => k === 'QUOTE_ACCEPTED')?.[1] || 0}
              </p>
              <p className="text-xs text-gray-500">Listas para producción</p>
            </div>

            <div className="space-y-2 p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-gray-600">ROI (Estimado)</p>
              <p className="text-2xl font-bold text-purple-600">
                {summary.total_ingresos > 0 && summary.total_estimated_value > 0
                  ? (
                      ((summary.total_ingresos - summary.total_estimated_value) /
                        summary.total_estimated_value) *
                      100
                    ).toFixed(1)
                  : 0}
                %
              </p>
              <p className="text-xs text-gray-500">Margen teórico</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

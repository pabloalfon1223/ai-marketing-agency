import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { produccionAPI, type Produccion } from '../api/produccion';
import { dashboardsAPI } from '../api/dashboards';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Package, TrendingUp, Calendar, DollarSign } from 'lucide-react';

const ESTADOS = [
  { value: 'ACCEPTED', label: 'Aceptada', color: 'bg-blue-100 text-blue-800' },
  { value: 'IN_PRODUCTION', label: 'En Producción', color: 'bg-orange-100 text-orange-800' },
  { value: 'COMPLETED', label: 'Completada', color: 'bg-purple-100 text-purple-800' },
  { value: 'DELIVERED', label: 'Entregada ✓', color: 'bg-green-100 text-green-800' },
];

export default function Produccion() {
  const [filterEstado, setFilterEstado] = useState<string | undefined>();
  const [searchCliente, setSearchCliente] = useState('');

  // Fetch produccion orders
  const { data: ordenes = [], isLoading, error } = useQuery({
    queryKey: ['produccion', filterEstado],
    queryFn: () => produccionAPI.list(filterEstado),
    refetchInterval: 30000,
  });

  // Fetch timeline data
  const { data: timelineData = [] } = useQuery({
    queryKey: ['dashboards-timeline'],
    queryFn: () => dashboardsAPI.timelineProduccion(),
    refetchInterval: 30000,
  });

  // Fetch ingresos
  const { data: ingresosData } = useQuery({
    queryKey: ['dashboards-ingresos'],
    queryFn: () => dashboardsAPI.ingresosTotal(),
    refetchInterval: 30000,
  });

  // Calculate stats
  const stats = {
    total: ordenes.length,
    enProduccion: ordenes.filter(o => o.estado === 'IN_PRODUCTION').length,
    completadas: ordenes.filter(o => o.estado === 'COMPLETED').length,
    entregadas: ordenes.filter(o => o.estado === 'DELIVERED').length,
    totalIngresos: ingresosData?.total_ingresos || 0,
    promedioDias: ordenes.length > 0
      ? Math.round(
          ordenes
            .filter(o => o.fecha_entrega_est && o.fecha_inicio)
            .reduce((sum, o) => {
              const inicio = new Date(o.fecha_inicio).getTime();
              const fin = new Date(o.fecha_entrega_est!).getTime();
              return sum + (fin - inicio) / (1000 * 60 * 60 * 24);
            }, 0) / ordenes.length
        )
      : 0,
  };

  // Filter ordenes
  const filteredOrdenes = ordenes.filter(o =>
    o.cliente.toLowerCase().includes(searchCliente.toLowerCase())
  );

  const getEstadoColor = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.color || 'bg-gray-100 text-gray-800';
  };

  const getEstadoLabel = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.label || estado;
  };

  const calcularDias = (inicio: string, fin?: string) => {
    if (!fin) return '-';
    const start = new Date(inicio).getTime();
    const end = new Date(fin).getTime();
    const dias = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    return `${dias}d`;
  };

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Producción</h1>
        <p className="text-gray-600 mt-2">Seguimiento de órdenes de producción y entregas</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Órdenes</CardTitle>
            <Package className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-gray-600">Órdenes en sistema</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">En Producción</CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.enProduccion}</div>
            <p className="text-xs text-gray-600">Activamente siendo producidas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ingresos Completados</CardTitle>
            <DollarSign className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ARS {stats.totalIngresos.toLocaleString('es-AR')}
            </div>
            <p className="text-xs text-gray-600">Entregadas completadas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Promedio de Días</CardTitle>
            <Calendar className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.promedioDias}d</div>
            <p className="text-xs text-gray-600">Tiempo promedio producción</p>
          </CardContent>
        </Card>
      </div>

      {/* Estado Breakdown */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Aceptadas', count: ordenes.filter(o => o.estado === 'ACCEPTED').length, color: 'text-blue-600' },
          { label: 'En Producción', count: stats.enProduccion, color: 'text-orange-600' },
          { label: 'Completadas', count: stats.completadas, color: 'text-purple-600' },
          { label: 'Entregadas', count: stats.entregadas, color: 'text-green-600' },
        ].map(item => (
          <Card key={item.label}>
            <CardContent className="pt-6">
              <div className={`text-3xl font-bold ${item.color}`}>{item.count}</div>
              <p className="text-sm text-gray-600 mt-1">{item.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <Input
          placeholder="Buscar por cliente..."
          value={searchCliente}
          onChange={(e) => setSearchCliente(e.target.value)}
          className="flex-1"
        />
        <Select value={filterEstado || ''} onValueChange={(v) => setFilterEstado(v || undefined)}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filtrar por estado" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todos los estados</SelectItem>
            {ESTADOS.map(e => (
              <SelectItem key={e.value} value={e.value}>{e.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Produccion Table */}
      <Card>
        <CardHeader>
          <CardTitle>Órdenes de Producción</CardTitle>
          <CardDescription>{filteredOrdenes.length} órdenes encontradas</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
              Error al cargar órdenes
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50">
                    <TableHead>Orden ID</TableHead>
                    <TableHead>Cliente</TableHead>
                    <TableHead>Mueble</TableHead>
                    <TableHead>Estado</TableHead>
                    <TableHead>Inicio</TableHead>
                    <TableHead>Entrega Est.</TableHead>
                    <TableHead>Días</TableHead>
                    <TableHead>Precio Final</TableHead>
                    <TableHead>Productor</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredOrdenes.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={9} className="text-center py-8 text-gray-500">
                        No hay órdenes encontradas
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredOrdenes.map(orden => (
                      <TableRow key={orden.id} className="hover:bg-gray-50">
                        <TableCell className="font-mono font-semibold">{orden.orden_id}</TableCell>
                        <TableCell className="font-medium">{orden.cliente}</TableCell>
                        <TableCell>{orden.mueble}</TableCell>
                        <TableCell>
                          <Badge className={getEstadoColor(orden.estado)}>
                            {getEstadoLabel(orden.estado)}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm">
                          {new Date(orden.fecha_inicio).toLocaleDateString('es-AR')}
                        </TableCell>
                        <TableCell className="text-sm">
                          {orden.fecha_entrega_est
                            ? new Date(orden.fecha_entrega_est).toLocaleDateString('es-AR')
                            : '-'}
                        </TableCell>
                        <TableCell className="font-semibold">
                          {calcularDias(orden.fecha_inicio, orden.fecha_entrega_est)}
                        </TableCell>
                        <TableCell className="font-semibold">
                          ARS {orden.precio_final.toLocaleString('es-AR')}
                        </TableCell>
                        <TableCell>{orden.productor}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

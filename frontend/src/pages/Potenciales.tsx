import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { potencialesAPI, type Potencial } from '../api/potenciales';
import { dashboardsAPI } from '../api/dashboards';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Search, TrendingUp, Target, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

// Estados con colores actualizados
const ESTADOS = [
  { value: 'SIN_RESPUESTA', label: 'Sin Respuesta', color: 'bg-gray-100 text-gray-800' },
  { value: 'ESPERAMOS_RESPUESTA', label: 'Esperamos Respuesta', color: 'bg-orange-100 text-orange-800' },
  { value: 'COTIZACION_ENVIADA', label: 'Cotización Enviada', color: 'bg-blue-100 text-blue-800' },
  { value: 'CLIENTE', label: '✅ Cliente', color: 'bg-green-100 text-green-800' },
  { value: 'CERRAR', label: 'Cerrar', color: 'bg-red-100 text-red-800' },
  { value: 'RECONTACTAR', label: 'Recontactar', color: 'bg-red-100 text-red-800' },
];

const PRIORIDADES = [
  { value: 'ALTA', label: 'ALTA', color: 'bg-red-100 text-red-800' },
  { value: 'MEDIA', label: 'MEDIA', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'BAJA', label: 'BAJA', color: 'bg-green-100 text-green-800' },
];

interface Stats {
  total: number;
  sinRespuesta: number;
  esperamos: number;
  cotizacion: number;
  clientes: number;
  conversionRate: number;
  cerrar: number;
  recontactar: number;
}

export default function Potenciales() {
  const [filterEstado, setFilterEstado] = useState<string | undefined>();
  const [filterPrioridad, setFilterPrioridad] = useState<string | undefined>();
  const [searchName, setSearchName] = useState('');

  // Fetch potenciales
  const { data: potencialesData = { total: 0, items: [] }, isLoading } = useQuery({
    queryKey: ['potenciales', filterEstado, filterPrioridad],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filterEstado) params.append('estado', filterEstado);
      if (filterPrioridad) params.append('prioridad', filterPrioridad);
      const res = await fetch(`/api/v1/potenciales?${params}`);
      return res.json();
    },
    refetchInterval: 30000,
  });

  const potenciales = potencialesData.items || [];

  // Fetch conversion rate
  const { data: conversionData } = useQuery({
    queryKey: ['dashboards-conversion-rate'],
    queryFn: async () => {
      const res = await fetch('/api/v1/dashboards/potenciales/conversion-rate');
      return res.json();
    },
    refetchInterval: 30000,
  });

  // Calculate stats
  const stats: Stats = useMemo(() => {
    const total = potenciales.length;
    const sinRespuesta = potenciales.filter((p: Potencial) => p.estado === 'SIN_RESPUESTA').length;
    const esperamos = potenciales.filter((p: Potencial) => p.estado === 'ESPERAMOS_RESPUESTA').length;
    const cotizacion = potenciales.filter((p: Potencial) => p.estado === 'COTIZACION_ENVIADA').length;
    const clientes = potenciales.filter((p: Potencial) => p.estado === 'CLIENTE').length;
    const cerrar = potenciales.filter((p: Potencial) => p.estado === 'CERRAR').length;
    const recontactar = potenciales.filter((p: Potencial) => p.estado === 'RECONTACTAR').length;
    const conversionRate = total > 0 ? (clientes / total) * 100 : 0;

    return {
      total,
      sinRespuesta,
      esperamos,
      cotizacion,
      clientes,
      conversionRate,
      cerrar,
      recontactar,
    };
  }, [potenciales]);

  // Filter potenciales
  const filteredPotenciales = potenciales.filter((p: Potencial) =>
    (p.nombre.toLowerCase().includes(searchName.toLowerCase()) ||
     p.celular?.includes(searchName))
  );

  const getEstadoColor = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.color || 'bg-gray-100 text-gray-800';
  };

  const getEstadoLabel = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.label || estado;
  };

  const getPrioridadColor = (prioridad: string) => {
    const found = PRIORIDADES.find(p => p.value === prioridad);
    return found?.color || 'bg-gray-100 text-gray-800';
  };

  const getPrioridadLabel = (prioridad: string) => {
    const found = PRIORIDADES.find(p => p.value === prioridad);
    return found?.label || prioridad;
  };

  const formatFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-AR');
  };

  return (
    <div className="space-y-6 p-4 md:p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Potenciales</h1>
        <p className="text-gray-600 mt-2">Gestión de clientes potenciales y seguimiento de ventas</p>
      </div>

      {/* Stats Cards - Responsive Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Potenciales</CardTitle>
            <Target className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-gray-600">En total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clientes ✅</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.clientes}</div>
            <p className="text-xs text-gray-600">Convertidos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tasa Conversión</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.conversionRate.toFixed(1)}%</div>
            <p className="text-xs text-gray-600">{stats.clientes} de {stats.total}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Esperando Respuesta</CardTitle>
            <AlertCircle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.esperamos}</div>
            <p className="text-xs text-gray-600">Requieren seguimiento</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters - Responsive Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="relative">
          <Search className="absolute left-2 top-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Buscar por nombre o celular..."
            value={searchName}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchName(e.target.value)}
            className="pl-8"
          />
        </div>
        <Select value={filterEstado || ''} onValueChange={(v: string) => setFilterEstado(v || undefined)}>
          <SelectTrigger>
            <SelectValue placeholder="Filtrar por estado" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todos los estados</SelectItem>
            {ESTADOS.map(e => (
              <SelectItem key={e.value} value={e.value}>{e.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={filterPrioridad || ''} onValueChange={(v: string) => setFilterPrioridad(v || undefined)}>
          <SelectTrigger>
            <SelectValue placeholder="Filtrar por prioridad" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todas las prioridades</SelectItem>
            {PRIORIDADES.map(p => (
              <SelectItem key={p.value} value={p.value}>{p.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Potenciales Table */}
      <Card>
        <CardHeader>
          <CardTitle>Lista de Potenciales</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50">
                    <TableHead className="whitespace-nowrap">Nombre</TableHead>
                    <TableHead className="whitespace-nowrap">Mueble</TableHead>
                    <TableHead className="whitespace-nowrap">Celular</TableHead>
                    <TableHead className="whitespace-nowrap">Estado</TableHead>
                    <TableHead className="whitespace-nowrap">Prioridad</TableHead>
                    <TableHead className="whitespace-nowrap">Fecha</TableHead>
                    <TableHead className="whitespace-nowrap">Vendedor</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPotenciales.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} className="text-center py-8 text-gray-500">
                        No hay potenciales encontrados
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredPotenciales.map((potencial: Potencial) => (
                      <TableRow key={potencial.id} className="hover:bg-gray-50 cursor-pointer">
                        <TableCell className="font-medium">{potencial.nombre}</TableCell>
                        <TableCell className="text-sm">{potencial.mueble}</TableCell>
                        <TableCell className="text-sm">{potencial.celular || '-'}</TableCell>
                        <TableCell>
                          <Badge className={getEstadoColor(potencial.estado)}>
                            {getEstadoLabel(potencial.estado)}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge className={getPrioridadColor(potencial.prioridad)}>
                            {getPrioridadLabel(potencial.prioridad)}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm">{formatFecha(potencial.fecha)}</TableCell>
                        <TableCell className="text-sm">{potencial.quien_lo_tiene || '-'}</TableCell>
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

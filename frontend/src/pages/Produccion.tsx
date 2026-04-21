import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { produccionAPI, type Produccion } from '../api/produccion';
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
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Search, AlertTriangle, Clock, CheckCircle2, Loader2 } from 'lucide-react';

// 8 Estados válidos de PRODUCCION
const ESTADOS_PRODUCCION = [
  { value: 'PLANIFICACIÓN', label: 'Planificación', color: 'bg-orange-100 text-orange-800' },
  { value: 'CARPINTERIA', label: 'Carpintería', color: 'bg-blue-100 text-blue-800' },
  { value: 'LAQUEADO', label: 'Laqueado', color: 'bg-purple-100 text-purple-800' },
  { value: 'RETIRO PARA REMODELAR', label: 'Retiro para Remodelar', color: 'bg-pink-100 text-pink-800' },
  { value: 'PENDIENTE', label: 'Pendiente', color: 'bg-red-100 text-red-800' },
  { value: 'POST VENTA', label: 'Post Venta', color: 'bg-cyan-100 text-cyan-800' },
  { value: 'FIDELIZACION', label: 'Fidelización', color: 'bg-indigo-100 text-indigo-800' },
  { value: 'FINALIZADO', label: 'Finalizado', color: 'bg-green-100 text-green-800' },
];

interface Stats {
  total: number;
  finalizados: number;
  alertas5Dias: number;
}

export default function Produccion() {
  const [filterEstado, setFilterEstado] = useState<string | undefined>();
  const [searchCliente, setSearchCliente] = useState('');

  // Fetch producción
  const { data: produccionData = { total: 0, items: [] }, isLoading } = useQuery({
    queryKey: ['produccion', filterEstado],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filterEstado) params.append('estado', filterEstado);
      const res = await fetch(`/api/v1/produccion?${params}`);
      return res.json();
    },
    refetchInterval: 30000,
  });

  const produccionItems = produccionData.items || [];

  // Calculate stats
  const stats: Stats = useMemo(() => {
    const total = produccionItems.length;
    const finalizados = produccionItems.filter((p: Produccion) => p.estado === 'FINALIZADO').length;

    // Contar registros sin actualizar > 5 días
    const now = new Date();
    const alertas5Dias = produccionItems.filter((p: Produccion) => {
      const updated = new Date(p.updated_at);
      const diasDiferencia = Math.floor((now.getTime() - updated.getTime()) / (1000 * 60 * 60 * 24));
      return diasDiferencia > 5;
    }).length;

    return {
      total,
      finalizados,
      alertas5Dias,
    };
  }, [produccionItems]);

  // Filter producción
  const filteredProduccion = produccionItems.filter((p: Produccion) =>
    p.cliente.toLowerCase().includes(searchCliente.toLowerCase()) ||
    p.celular?.includes(searchCliente)
  );

  const getEstadoColor = (estado: string) => {
    const found = ESTADOS_PRODUCCION.find(e => e.value === estado);
    return found?.color || 'bg-gray-100 text-gray-800';
  };

  const getEstadoLabel = (estado: string) => {
    const found = ESTADOS_PRODUCCION.find(e => e.value === estado);
    return found?.label || estado;
  };

  const formatFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-AR');
  };

  const getDiasDesdeActualizacion = (updatedAt: string) => {
    const updated = new Date(updatedAt);
    const now = new Date();
    const diasDiferencia = Math.floor((now.getTime() - updated.getTime()) / (1000 * 60 * 60 * 24));
    return diasDiferencia;
  };

  const getAlertaColor = (diasSinActualizar: number) => {
    if (diasSinActualizar > 5) {
      return 'bg-red-50'; // Fondo rojo si > 5 días
    }
    return 'hover:bg-gray-50';
  };

  const getAlertaBadge = (diasSinActualizar: number) => {
    if (diasSinActualizar > 5) {
      return (
        <Badge className="bg-red-100 text-red-800">
          ⚠️ {diasSinActualizar} días sin actualizar
        </Badge>
      );
    }
    if (diasSinActualizar >= 3) {
      return (
        <Badge className="bg-orange-100 text-orange-800">
          ⚠️ {diasSinActualizar} días sin actualizar
        </Badge>
      );
    }
    return (
      <Badge className="bg-gray-100 text-gray-800">
        {diasSinActualizar} días
      </Badge>
    );
  };

  return (
    <div className="space-y-6 p-4 md:p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Producción</h1>
        <p className="text-gray-600 mt-2">Seguimiento de órdenes de producción</p>
      </div>

      {/* Stats Cards - Responsive Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Órdenes</CardTitle>
            <Clock className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-gray-600">En seguimiento</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Finalizadas</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.finalizados}</div>
            <p className="text-xs text-gray-600">Completadas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Alertas</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.alertas5Dias}</div>
            <p className="text-xs text-gray-600">Sin actualizar &gt;5 días</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters - Responsive Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="relative">
          <Search className="absolute left-2 top-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Buscar por cliente o celular..."
            value={searchCliente}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchCliente(e.target.value)}
            className="pl-8"
          />
        </div>
        <Select value={filterEstado || ''} onValueChange={(v: string) => setFilterEstado(v || undefined)}>
          <SelectTrigger>
            <SelectValue placeholder="Filtrar por estado" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todos los estados</SelectItem>
            {ESTADOS_PRODUCCION.map(e => (
              <SelectItem key={e.value} value={e.value}>{e.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Producción Table */}
      <Card>
        <CardHeader>
          <CardTitle>Órdenes de Producción</CardTitle>
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
                    <TableHead className="whitespace-nowrap">Cliente</TableHead>
                    <TableHead className="whitespace-nowrap">Celular</TableHead>
                    <TableHead className="whitespace-nowrap">Descripción</TableHead>
                    <TableHead className="whitespace-nowrap">Estado</TableHead>
                    <TableHead className="whitespace-nowrap">Actualizado</TableHead>
                    <TableHead className="whitespace-nowrap">Creado</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredProduccion.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center py-8 text-gray-500">
                        No hay órdenes encontradas
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredProduccion.map((orden: Produccion) => {
                      const diasSinActualizar = getDiasDesdeActualizacion(orden.updated_at);
                      return (
                        <TableRow
                          key={orden.id}
                          className={`cursor-pointer ${getAlertaColor(diasSinActualizar)}`}
                        >
                          <TableCell className="font-medium">{orden.cliente}</TableCell>
                          <TableCell className="text-sm">{orden.celular || '-'}</TableCell>
                          <TableCell className="text-sm">{orden.descripcion_breve || '-'}</TableCell>
                          <TableCell>
                            <Badge className={getEstadoColor(orden.estado)}>
                              {getEstadoLabel(orden.estado)}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            {getAlertaBadge(diasSinActualizar)}
                          </TableCell>
                          <TableCell className="text-sm">{formatFecha(orden.created_at)}</TableCell>
                        </TableRow>
                      );
                    })
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

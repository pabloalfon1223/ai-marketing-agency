import { useState, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, ArrowRight, TrendingUp, Target, DollarSign, Clock } from 'lucide-react';

const ESTADOS = [
  { value: 'SIN_RESPUESTA', label: 'Sin Respuesta', color: 'bg-gray-100 text-gray-800' },
  { value: 'ESPERAMOS_RESPUESTA', label: 'Esperamos Respuesta', color: 'bg-blue-100 text-blue-800' },
  { value: 'COTIZACION_ENVIADA', label: 'Cotización Enviada', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'QUOTE_ACCEPTED', label: 'Quote Accepted ✓', color: 'bg-green-100 text-green-800' },
];

interface Stats {
  total: number;
  sinRespuesta: number;
  esperamos: number;
  cotizacion: number;
  accepted: number;
  conversionRate: number;
  totalValue: number;
}

export default function Potenciales() {
  const queryClient = useQueryClient();
  const [filterEstado, setFilterEstado] = useState<string | undefined>();
  const [searchName, setSearchName] = useState('');

  // Fetch potenciales
  const { data: potenciales = [], isLoading, error } = useQuery({
    queryKey: ['potenciales', filterEstado],
    queryFn: () => potencialesAPI.list(filterEstado),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  // Fetch conversion rate
  const { data: conversionData } = useQuery({
    queryKey: ['dashboards-conversion-rate'],
    queryFn: () => dashboardsAPI.conversionRate(),
    refetchInterval: 30000,
  });

  // Fetch value by status
  const { data: valueByStatus = {} } = useQuery({
    queryKey: ['dashboards-value-by-status'],
    queryFn: () => dashboardsAPI.valueByStatus(),
    refetchInterval: 30000,
  });

  // Convert mutation
  const convertMutation = useMutation({
    mutationFn: (id: number) => potencialesAPI.convertToProduccion(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['potenciales'] });
      queryClient.invalidateQueries({ queryKey: ['dashboards-conversion-rate'] });
    },
  });

  // Calculate stats
  const stats: Stats = useMemo(() => {
    const total = potenciales.length;
    const sinRespuesta = potenciales.filter(p => p.estado === 'SIN_RESPUESTA').length;
    const esperamos = potenciales.filter(p => p.estado === 'ESPERAMOS_RESPUESTA').length;
    const cotizacion = potenciales.filter(p => p.estado === 'COTIZACION_ENVIADA').length;
    const accepted = potenciales.filter(p => p.estado === 'QUOTE_ACCEPTED').length;
    const conversionRate = total > 0 ? (accepted / total) * 100 : 0;
    const totalValue = potenciales.reduce((sum, p) => sum + p.valor_estimado, 0);

    return {
      total,
      sinRespuesta,
      esperamos,
      cotizacion,
      accepted,
      conversionRate,
      totalValue,
    };
  }, [potenciales]);

  // Filter potenciales
  const filteredPotenciales = potenciales.filter(p =>
    p.nombre.toLowerCase().includes(searchName.toLowerCase())
  );

  const getEstadoColor = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.color || 'bg-gray-100 text-gray-800';
  };

  const getEstadoLabel = (estado: string) => {
    const found = ESTADOS.find(e => e.value === estado);
    return found?.label || estado;
  };

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Potenciales</h1>
        <p className="text-gray-600 mt-2">Gestión de clientes potenciales y seguimiento de ventas</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.conversionRate.toFixed(1)}%</div>
            <p className="text-xs text-gray-600">{stats.accepted} de {stats.total}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Valor Total Estimado</CardTitle>
            <DollarSign className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">ARS {stats.totalValue.toLocaleString('es-AR')}</div>
            <p className="text-xs text-gray-600">Valor combinado</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">En Cotización</CardTitle>
            <Clock className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.cotizacion}</div>
            <p className="text-xs text-gray-600">Esperando respuesta</p>
          </CardContent>
        </Card>
      </div>

      {/* Funnel Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Funnel de Conversión</CardTitle>
          <CardDescription>Estado de los potenciales en el pipeline</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Sin Respuesta</span>
              <div className="flex items-center gap-2">
                <div className="w-48 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-400 h-2 rounded-full"
                    style={{ width: `${(stats.sinRespuesta / stats.total) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold w-12 text-right">{stats.sinRespuesta}</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Esperamos Respuesta</span>
              <div className="flex items-center gap-2">
                <div className="w-48 bg-blue-200 rounded-full h-2">
                  <div
                    className="bg-blue-400 h-2 rounded-full"
                    style={{ width: `${(stats.esperamos / stats.total) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold w-12 text-right">{stats.esperamos}</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Cotización Enviada</span>
              <div className="flex items-center gap-2">
                <div className="w-48 bg-yellow-200 rounded-full h-2">
                  <div
                    className="bg-yellow-400 h-2 rounded-full"
                    style={{ width: `${(stats.cotizacion / stats.total) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold w-12 text-right">{stats.cotizacion}</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Quote Accepted ✓</span>
              <div className="flex items-center gap-2">
                <div className="w-48 bg-green-200 rounded-full h-2">
                  <div
                    className="bg-green-400 h-2 rounded-full"
                    style={{ width: `${(stats.accepted / stats.total) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold w-12 text-right">{stats.accepted}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Filters */}
      <div className="flex gap-4">
        <Input
          placeholder="Buscar por nombre..."
          value={searchName}
          onChange={(e) => setSearchName(e.target.value)}
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

      {/* Potenciales Table */}
      <Card>
        <CardHeader>
          <CardTitle>Lista de Potenciales</CardTitle>
          <CardDescription>{filteredPotenciales.length} potenciales encontrados</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
              Error al cargar potenciales
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50">
                    <TableHead>Nombre</TableHead>
                    <TableHead>Mueble</TableHead>
                    <TableHead>Estado</TableHead>
                    <TableHead>Contacto</TableHead>
                    <TableHead>Valor Est.</TableHead>
                    <TableHead>Vendedor</TableHead>
                    <TableHead>Acciones</TableHead>
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
                    filteredPotenciales.map(potencial => (
                      <TableRow key={potencial.id} className="hover:bg-gray-50">
                        <TableCell className="font-medium">{potencial.nombre}</TableCell>
                        <TableCell>{potencial.mueble}</TableCell>
                        <TableCell>
                          <Badge className={getEstadoColor(potencial.estado)}>
                            {getEstadoLabel(potencial.estado)}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm">
                          {new Date(potencial.fecha_contacto).toLocaleDateString('es-AR')}
                        </TableCell>
                        <TableCell className="font-semibold">
                          ARS {potencial.valor_estimado.toLocaleString('es-AR')}
                        </TableCell>
                        <TableCell>{potencial.quien_lo_tiene}</TableCell>
                        <TableCell>
                          {potencial.estado === 'COTIZACION_ENVIADA' && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => convertMutation.mutate(potencial.id)}
                              disabled={convertMutation.isPending}
                              className="gap-1"
                            >
                              {convertMutation.isPending ? (
                                <Loader2 className="h-4 w-4 animate-spin" />
                              ) : (
                                <ArrowRight className="h-4 w-4" />
                              )}
                              Convertir
                            </Button>
                          )}
                          {potencial.estado === 'QUOTE_ACCEPTED' && (
                            <Badge className="bg-green-200 text-green-800">Convertido</Badge>
                          )}
                        </TableCell>
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

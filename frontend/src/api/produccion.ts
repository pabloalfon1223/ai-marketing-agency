import api from './client';

export interface Produccion {
  id: number;
  orden_id: string;
  cliente: string;
  mueble: string;
  estado: 'ACCEPTED' | 'IN_PRODUCTION' | 'COMPLETED' | 'DELIVERED';
  fecha_inicio: string;
  fecha_entrega_est?: string;
  productor: string;
  costo_real: number;
  precio_final: number;
  notas?: string;
  potencial_id?: number;
  created_at: string;
  updated_at: string;
}

export interface ProduccionCreate {
  orden_id: string;
  cliente: string;
  mueble: string;
  estado?: string;
  fecha_inicio: string;
  fecha_entrega_est?: string;
  productor: string;
  costo_real: number;
  precio_final: number;
  notas?: string;
  potencial_id?: number;
}

export interface ProduccionUpdate {
  orden_id?: string;
  cliente?: string;
  mueble?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_entrega_est?: string;
  productor?: string;
  costo_real?: number;
  precio_final?: number;
  notas?: string;
}

export const produccionAPI = {
  list: (estado?: string) =>
    api.get<Produccion[]>('/produccion', { params: { estado } }).then(r => r.data),

  getById: (orden_id: string) =>
    api.get<Produccion>(`/produccion/${orden_id}`).then(r => r.data),

  create: (data: ProduccionCreate) =>
    api.post<Produccion>('/produccion', data).then(r => r.data),

  update: (orden_id: string, data: ProduccionUpdate) =>
    api.put<Produccion>(`/produccion/${orden_id}`, data).then(r => r.data),
};

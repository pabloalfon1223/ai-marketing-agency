import api from './client';

export interface Potencial {
  id: number;
  nombre: string;
  mueble: string;
  fecha_contacto: string;
  estado: 'SIN_RESPUESTA' | 'ESPERAMOS_RESPUESTA' | 'COTIZACION_ENVIADA' | 'QUOTE_ACCEPTED';
  quien_lo_tiene: string;
  telefono: string;
  nota?: string;
  fecha_seguimiento?: string;
  valor_estimado: number;
  orden_id_asignada?: string;
  created_at: string;
  updated_at: string;
}

export interface PotencialCreate {
  nombre: string;
  mueble: string;
  fecha_contacto: string;
  estado?: string;
  quien_lo_tiene: string;
  telefono: string;
  nota?: string;
  fecha_seguimiento?: string;
  valor_estimado: number;
}

export interface PotencialUpdate {
  nombre?: string;
  mueble?: string;
  fecha_contacto?: string;
  estado?: string;
  quien_lo_tiene?: string;
  telefono?: string;
  nota?: string;
  fecha_seguimiento?: string;
  valor_estimado?: number;
}

export const potencialesAPI = {
  list: (estado?: string) =>
    api.get<Potencial[]>('/potenciales', { params: { estado } }).then(r => r.data),

  getById: (id: number) =>
    api.get<Potencial>(`/potenciales/${id}`).then(r => r.data),

  create: (data: PotencialCreate) =>
    api.post<Potencial>('/potenciales', data).then(r => r.data),

  update: (id: number, data: PotencialUpdate) =>
    api.put<Potencial>(`/potenciales/${id}`, data).then(r => r.data),

  convertToProduccion: (id: number) =>
    api.post(`/potenciales/${id}/convert`, {}).then(r => r.data),
};

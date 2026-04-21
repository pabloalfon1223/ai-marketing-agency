import api from './client';
import type { Client } from '../types';

export const getClients = () => api.get<Client[]>('/clients').then(r => r.data);
export const getClient = (id: number) => api.get<Client>(`/clients/${id}`).then(r => r.data);
export const createClient = (data: Partial<Client>) => api.post<Client>('/clients', data).then(r => r.data);
export const updateClient = (id: number, data: Partial<Client>) => api.put<Client>(`/clients/${id}`, data).then(r => r.data);
export const deleteClient = (id: number) => api.delete(`/clients/${id}`);

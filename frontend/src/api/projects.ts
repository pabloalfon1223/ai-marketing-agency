import api from './client';
import type { Project } from '../types';

export const getProjects = (clientId?: number) =>
  api.get<Project[]>('/projects', { params: clientId ? { client_id: clientId } : {} }).then(r => r.data);
export const getProject = (id: number) => api.get<Project>(`/projects/${id}`).then(r => r.data);
export const createProject = (data: Partial<Project>) => api.post<Project>('/projects', data).then(r => r.data);
export const updateProject = (id: number, data: Partial<Project>) => api.put<Project>(`/projects/${id}`, data).then(r => r.data);
export const deleteProject = (id: number) => api.delete(`/projects/${id}`);

export function formatDate(date: string | null): string {
  if (!date) return '-';
  return new Date(date).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

export function formatDateTime(date: string | null): string {
  if (!date) return '-';
  return new Date(date).toLocaleString('es-ES', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function statusColor(status: string): string {
  const colors: Record<string, string> = {
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    running: 'bg-yellow-100 text-yellow-800',
    pending: 'bg-gray-100 text-gray-800',
    failed: 'bg-red-100 text-red-800',
    draft: 'bg-gray-100 text-gray-600',
    review: 'bg-orange-100 text-orange-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    published: 'bg-purple-100 text-purple-800',
    planning: 'bg-indigo-100 text-indigo-800',
    paused: 'bg-yellow-100 text-yellow-700',
    idle: 'bg-gray-100 text-gray-600',
    busy: 'bg-yellow-100 text-yellow-800',
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
}

export const agentDisplayNames: Record<string, string> = {
  orchestrator: 'Orquestador',
  strategy: 'Estrategia',
  content: 'Contenido',
  seo: 'SEO',
  social_media: 'Redes Sociales',
  email_marketing: 'Email Marketing',
  analytics: 'Analytics',
  branding: 'Branding',
  advertising: 'Publicidad',
};

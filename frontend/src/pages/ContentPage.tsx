import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Check, X, RefreshCw, Eye } from 'lucide-react';
import Header from '../components/layout/Header';
import Modal from '../components/shared/Modal';
import StatusBadge from '../components/shared/StatusBadge';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import { getContents, updateContentStatus, regenerateContent } from '../api/content';
import { formatDateTime } from '../utils/formatters';
import type { Content } from '../types';

const FILTERS = ['all', 'draft', 'review', 'approved', 'rejected', 'published'];

export default function ContentPage() {
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState('all');
  const { data: contents, isLoading } = useQuery({
    queryKey: ['content', statusFilter],
    queryFn: () => getContents(statusFilter !== 'all' ? { status: statusFilter } : {}),
  });
  const [viewContent, setViewContent] = useState<Content | null>(null);
  const [reviewNotes, setReviewNotes] = useState('');

  const approveMut = useMutation({
    mutationFn: (id: number) => updateContentStatus(id, { status: 'approved', review_notes: reviewNotes }),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['content'] }); setViewContent(null); },
  });
  const rejectMut = useMutation({
    mutationFn: (id: number) => updateContentStatus(id, { status: 'rejected', review_notes: reviewNotes }),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['content'] }); setViewContent(null); },
  });
  const regenMut = useMutation({
    mutationFn: regenerateContent,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['content'] }),
  });

  return (
    <>
      <Header title="Contenido" />
      <div className="p-6 space-y-4">
        {/* Filters */}
        <div className="flex gap-2">
          {FILTERS.map(f => (
            <button key={f} onClick={() => setStatusFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                statusFilter === f ? 'bg-primary-600 text-white border-primary-600' : 'bg-white text-gray-600 border-gray-300 hover:border-primary-400'
              }`}>
              {f === 'all' ? 'Todos' : f}
            </button>
          ))}
        </div>

        {/* Content List */}
        {isLoading ? <LoadingSpinner /> : (
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Titulo</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Tipo</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Plataforma</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">SEO</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {contents?.map((c: Content) => (
                  <tr key={c.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium max-w-xs truncate">{c.title || 'Sin titulo'}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">{c.content_type || '-'}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">{c.platform || '-'}</td>
                    <td className="px-6 py-4"><StatusBadge status={c.status} /></td>
                    <td className="px-6 py-4">
                      {c.seo_score != null ? (
                        <span className={`text-sm font-medium ${c.seo_score >= 70 ? 'text-green-600' : c.seo_score >= 40 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {c.seo_score.toFixed(0)}
                        </span>
                      ) : '-'}
                    </td>
                    <td className="px-6 py-4 text-xs text-gray-500">{formatDateTime(c.created_at)}</td>
                    <td className="px-6 py-4 text-right">
                      <button onClick={() => { setViewContent(c); setReviewNotes(''); }} className="text-gray-400 hover:text-primary-600 mr-2">
                        <Eye size={16} />
                      </button>
                      <button onClick={() => regenMut.mutate(c.id)} className="text-gray-400 hover:text-orange-600">
                        <RefreshCw size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
                {!contents?.length && (
                  <tr><td colSpan={7} className="px-6 py-8 text-center text-sm text-gray-400">
                    No hay contenido generado. Lanza una campana o ejecuta un agente de contenido.
                  </td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Content Review Modal */}
      <Modal open={!!viewContent} onClose={() => setViewContent(null)} title="Revisar Contenido">
        {viewContent && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-2">
              <StatusBadge status={viewContent.status} />
              {viewContent.content_type && <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">{viewContent.content_type}</span>}
              {viewContent.platform && <span className="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded">{viewContent.platform}</span>}
            </div>
            <h4 className="font-semibold">{viewContent.title || 'Sin titulo'}</h4>
            <div className="bg-gray-50 rounded-lg p-4 max-h-60 overflow-y-auto">
              <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">{viewContent.body || 'Sin contenido'}</pre>
            </div>
            {viewContent.seo_score != null && (
              <div className="flex items-center gap-2 text-sm">
                <span className="text-gray-500">SEO Score:</span>
                <span className={`font-bold ${viewContent.seo_score >= 70 ? 'text-green-600' : 'text-yellow-600'}`}>
                  {viewContent.seo_score.toFixed(0)}/100
                </span>
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notas de revision</label>
              <textarea value={reviewNotes} onChange={e => setReviewNotes(e.target.value)} rows={2}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <button onClick={() => rejectMut.mutate(viewContent.id)}
                className="flex items-center gap-1 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700">
                <X size={14} /> Rechazar
              </button>
              <button onClick={() => approveMut.mutate(viewContent.id)}
                className="flex items-center gap-1 px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700">
                <Check size={14} /> Aprobar
              </button>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}

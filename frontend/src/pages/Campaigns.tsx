import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Rocket, Trash2, ChevronRight } from 'lucide-react';
import Header from '../components/layout/Header';
import Modal from '../components/shared/Modal';
import StatusBadge from '../components/shared/StatusBadge';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import { getCampaigns, createCampaign, deleteCampaign, launchCampaign } from '../api/campaigns';
import { getProjects } from '../api/projects';
import { formatDate } from '../utils/formatters';
import type { Campaign } from '../types';

const CAMPAIGN_TYPES = ['integrated', 'social', 'email', 'content', 'ads'];
const CHANNELS = ['instagram', 'linkedin', 'twitter', 'facebook', 'tiktok', 'email', 'blog', 'google_ads'];

export default function Campaigns() {
  const queryClient = useQueryClient();
  const { data: campaigns, isLoading } = useQuery({ queryKey: ['campaigns'], queryFn: () => getCampaigns() });
  const { data: projects } = useQuery({ queryKey: ['projects'], queryFn: () => getProjects() });
  const [modalOpen, setModalOpen] = useState(false);
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    project_id: 0, name: '', campaign_type: 'integrated',
    budget: '', target_channels: [] as string[],
    start_date: '', end_date: '',
  });
  const [detail, setDetail] = useState<Campaign | null>(null);

  const createMut = useMutation({
    mutationFn: createCampaign,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['campaigns'] }); closeModal(); },
  });
  const launchMut = useMutation({
    mutationFn: launchCampaign,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['campaigns', 'tasks'] }),
  });
  const deleteMut = useMutation({
    mutationFn: deleteCampaign,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['campaigns'] }),
  });

  function openNew() {
    setForm({ project_id: projects?.[0]?.id || 0, name: '', campaign_type: 'integrated', budget: '', target_channels: [], start_date: '', end_date: '' });
    setStep(1);
    setModalOpen(true);
  }
  function closeModal() { setModalOpen(false); setDetail(null); }

  function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    createMut.mutate({
      ...form,
      budget: form.budget ? Number(form.budget) : undefined,
      target_channels: JSON.stringify(form.target_channels),
      start_date: form.start_date || undefined,
      end_date: form.end_date || undefined,
    } as any);
  }

  function toggleChannel(ch: string) {
    setForm(f => ({
      ...f,
      target_channels: f.target_channels.includes(ch)
        ? f.target_channels.filter(c => c !== ch)
        : [...f.target_channels, ch]
    }));
  }

  const projectName = (id: number) => projects?.find((p: any) => p.id === id)?.name || '-';

  return (
    <>
      <Header title="Campanas" />
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <p className="text-sm text-gray-500">{campaigns?.length ?? 0} campanas</p>
          <button onClick={openNew} className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700">
            <Plus size={16} /> Nueva Campana
          </button>
        </div>

        {isLoading ? <LoadingSpinner /> : (
          <div className="grid gap-4">
            {campaigns?.map((c: Campaign) => (
              <div key={c.id} className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-sm transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold">{c.name}</h3>
                      <StatusBadge status={c.status} />
                      {c.campaign_type && (
                        <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">{c.campaign_type}</span>
                      )}
                    </div>
                    <div className="flex gap-4 text-xs text-gray-500">
                      <span>Proyecto: {projectName(c.project_id)}</span>
                      {c.budget && <span>Budget: ${c.budget.toLocaleString()}</span>}
                      <span>Creado: {formatDate(c.created_at)}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {c.status === 'draft' && (
                      <button onClick={() => launchMut.mutate(c.id)}
                        className="flex items-center gap-1 bg-green-600 text-white px-3 py-1.5 rounded-lg text-xs font-medium hover:bg-green-700">
                        <Rocket size={14} /> Lanzar
                      </button>
                    )}
                    <button onClick={() => deleteMut.mutate(c.id)} className="text-gray-400 hover:text-red-600 p-1">
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            {!campaigns?.length && (
              <div className="bg-white rounded-xl border border-gray-200 p-12 text-center text-sm text-gray-400">
                No hay campanas. Crea la primera para que los agentes IA trabajen.
              </div>
            )}
          </div>
        )}
      </div>

      {/* Campaign Creation Wizard */}
      <Modal open={modalOpen} onClose={closeModal} title={`Nueva Campana - Paso ${step}/3`}>
        <form onSubmit={handleCreate}>
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Proyecto *</label>
                <select required value={form.project_id} onChange={e => setForm({ ...form, project_id: Number(e.target.value) })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option value={0} disabled>Seleccionar proyecto</option>
                  {projects?.map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre de la campana *</label>
                <input required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                <div className="flex flex-wrap gap-2">
                  {CAMPAIGN_TYPES.map(t => (
                    <button key={t} type="button" onClick={() => setForm({ ...form, campaign_type: t })}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                        form.campaign_type === t ? 'bg-primary-600 text-white border-primary-600' : 'bg-white text-gray-600 border-gray-300 hover:border-primary-400'
                      }`}>
                      {t}
                    </button>
                  ))}
                </div>
              </div>
              <div className="flex justify-end pt-2">
                <button type="button" onClick={() => setStep(2)} className="flex items-center gap-1 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
                  Siguiente <ChevronRight size={16} />
                </button>
              </div>
            </div>
          )}
          {step === 2 && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Canales</label>
                <div className="flex flex-wrap gap-2">
                  {CHANNELS.map(ch => (
                    <button key={ch} type="button" onClick={() => toggleChannel(ch)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                        form.target_channels.includes(ch) ? 'bg-primary-600 text-white border-primary-600' : 'bg-white text-gray-600 border-gray-300 hover:border-primary-400'
                      }`}>
                      {ch}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Presupuesto (USD)</label>
                <input type="number" value={form.budget} onChange={e => setForm({ ...form, budget: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Inicio</label>
                  <input type="date" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Fin</label>
                  <input type="date" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
                </div>
              </div>
              <div className="flex justify-between pt-2">
                <button type="button" onClick={() => setStep(1)} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Atras</button>
                <button type="button" onClick={() => setStep(3)} className="flex items-center gap-1 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
                  Siguiente <ChevronRight size={16} />
                </button>
              </div>
            </div>
          )}
          {step === 3 && (
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                <p><span className="font-medium">Nombre:</span> {form.name}</p>
                <p><span className="font-medium">Tipo:</span> {form.campaign_type}</p>
                <p><span className="font-medium">Canales:</span> {form.target_channels.join(', ') || 'Ninguno'}</p>
                {form.budget && <p><span className="font-medium">Budget:</span> ${Number(form.budget).toLocaleString()}</p>}
                {form.start_date && <p><span className="font-medium">Periodo:</span> {form.start_date} - {form.end_date || '...'}</p>}
              </div>
              <p className="text-xs text-gray-500">Al crear la campana, podras lanzarla para que los agentes IA comiencen a trabajar automaticamente.</p>
              <div className="flex justify-between pt-2">
                <button type="button" onClick={() => setStep(2)} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Atras</button>
                <button type="submit" className="flex items-center gap-1 px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700">
                  <Rocket size={16} /> Crear Campana
                </button>
              </div>
            </div>
          )}
        </form>
      </Modal>
    </>
  );
}

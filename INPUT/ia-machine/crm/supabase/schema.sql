-- ============================================================
-- IA MACHINE — Schema Supabase
-- Ejecutar en: Supabase Dashboard → SQL Editor → Run
-- ============================================================

-- ============================================================
-- PROJECTS
-- ============================================================
create table if not exists projects (
  id text primary key,                        -- 'mente-pausada' | 'polt-mobilier' | 'cerebro'
  name text not null,
  priority int not null default 3,
  status_pct int not null default 0,
  currency text not null default 'USD',       -- 'USD' | 'ARS'
  revenue_month numeric not null default 0,
  revenue_goal numeric not null default 0,
  blockers jsonb not null default '[]',       -- ["texto blocker 1", ...]
  pending_tasks jsonb not null default '[]',  -- ["tarea 1", ...]
  meta jsonb not null default '{}',           -- datos extra por proyecto
  updated_at timestamptz not null default now()
);

-- ============================================================
-- AGENTS — se auto-registran cuando son creados
-- ============================================================
create table if not exists agents (
  id text primary key,                        -- 'content-director-mp'
  name text not null,
  description text,
  project_id text references projects(id) on delete cascade,
  status text not null default 'idle'         -- 'idle' | 'running' | 'active' | 'error'
    check (status in ('idle','running','active','error')),
  schedule text,                              -- '07:00 ARG' | 'Manual' | 'Lunes 09:00 ARG'
  trigger_id text,                            -- ID del remote trigger de Anthropic
  skill_base text,                            -- skill que usa como base
  prompt text,                                -- instrucciones del agente
  enabled bool not null default false,
  runs_total int not null default 0,
  runs_success int not null default 0,
  last_run_at timestamptz,
  next_run_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ============================================================
-- RUNS — cada ejecución de un agente queda registrada
-- ============================================================
create table if not exists runs (
  id uuid primary key default gen_random_uuid(),
  agent_id text references agents(id) on delete cascade,
  project_id text references projects(id),
  status text not null default 'running'
    check (status in ('running','success','error')),
  triggered_by text not null default 'manual'  -- 'manual' | 'schedule' | 'system'
    check (triggered_by in ('manual','schedule','system')),
  input jsonb,                                 -- parámetros de entrada
  output jsonb,                                -- resultado del agente
  logs jsonb not null default '[]',            -- ["[07:00] mensaje", ...]
  error_msg text,
  duration_ms int,
  started_at timestamptz not null default now(),
  finished_at timestamptz
);

-- ============================================================
-- CONTACTS — CRM unificado para los 3 proyectos
-- ============================================================
create table if not exists contacts (
  id uuid primary key default gen_random_uuid(),
  project_id text references projects(id) on delete cascade,
  name text not null,
  email text,
  phone text,
  stage text not null default 'nuevo'
    check (stage in ('nuevo','calificado','propuesta','negociacion','cerrado-ganado','cerrado-perdido')),
  value numeric not null default 0,
  currency text not null default 'USD',
  notes text,
  tags text[] not null default '{}',
  source text,                                 -- 'whatsapp' | 'instagram' | 'web' | 'manual'
  assigned_agent text references agents(id),   -- agente que lo gestiona
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ============================================================
-- STATE — estado global del sistema (1 fila por proyecto)
-- ============================================================
create table if not exists system_state (
  id text primary key default 'global',
  version text not null default '1.0',
  active_projects text[] not null default '{}',
  system_health text not null default 'operational',
  integrations jsonb not null default '{}',   -- { sendgrid: 'ok', hotmart: 'pending', ... }
  updated_at timestamptz not null default now()
);

-- ============================================================
-- INBOX — archivos pendientes de distribuir
-- ============================================================
create table if not exists inbox (
  id uuid primary key default gen_random_uuid(),
  project_id text references projects(id),
  filename text not null,
  file_type text,                              -- 'image' | 'audio' | 'video' | 'doc' | 'pdf'
  file_path text,
  status text not null default 'pending'
    check (status in ('pending','processed','distributed')),
  distributed_to text,                         -- carpeta destino
  notes text,
  created_at timestamptz not null default now(),
  processed_at timestamptz
);

-- ============================================================
-- CONTENT OUTPUT — lo que generan los agentes de contenido
-- ============================================================
create table if not exists content_output (
  id uuid primary key default gen_random_uuid(),
  project_id text references projects(id),
  agent_id text references agents(id),
  run_id uuid references runs(id),
  format text,                                 -- 'reel' | 'carrusel' | 'story' | 'post' | 'email'
  platform text,                              -- 'instagram' | 'tiktok' | 'email'
  hook text,
  body text,
  cta text,
  visual_prompt text,
  caption text,
  hashtags text[],
  status text not null default 'draft'
    check (status in ('draft','approved','published','rejected')),
  approved_by text,
  approved_at timestamptz,
  created_at timestamptz not null default now()
);

-- ============================================================
-- FUNCTIONS — actualización automática de updated_at
-- ============================================================
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger trg_projects_updated before update on projects
  for each row execute function update_updated_at();
create trigger trg_agents_updated before update on agents
  for each row execute function update_updated_at();
create trigger trg_contacts_updated before update on contacts
  for each row execute function update_updated_at();

-- ============================================================
-- RLS (Row Level Security) — solo el usuario autenticado accede
-- ============================================================
alter table projects enable row level security;
alter table agents enable row level security;
alter table runs enable row level security;
alter table contacts enable row level security;
alter table system_state enable row level security;
alter table inbox enable row level security;
alter table content_output enable row level security;

-- Policy: solo usuarios autenticados leen y escriben
create policy "auth_only" on projects for all using (auth.role() = 'authenticated');
create policy "auth_only" on agents for all using (auth.role() = 'authenticated');
create policy "auth_only" on runs for all using (auth.role() = 'authenticated');
create policy "auth_only" on contacts for all using (auth.role() = 'authenticated');
create policy "auth_only" on system_state for all using (auth.role() = 'authenticated');
create policy "auth_only" on inbox for all using (auth.role() = 'authenticated');
create policy "auth_only" on content_output for all using (auth.role() = 'authenticated');

-- ============================================================
-- SEED — datos iniciales del sistema
-- ============================================================
insert into projects (id, name, priority, status_pct, currency, revenue_month, revenue_goal, blockers, pending_tasks) values
('mente-pausada', 'Mente Pausada', 1, 80, 'USD', 0, 3000,
  '["Hotmart sin configurar — sin checkout no hay ventas","ruidomentalcero.com sin deploy"]',
  '["Configurar Hotmart + checkout ($47 USD)","Deploy ruidomentalcero.com","Activar Content Director 7AM","Primera campaña Meta Ads México"]'),
('polt-mobilier', 'Polt Mobilier', 2, 50, 'ARS', 320000, 2000000,
  '["WhatsApp bot Whapi.cloud sin configurar"]',
  '["Crear Google Sheet Polt Ops","Instalar Whapi.cloud bot","Completar Polt Calculator Pro","Pipeline de leads activo"]'),
('cerebro', 'Cerebro', 3, 0, 'USD', 0, 500,
  '["Market Scanner sin configurar","Supadata MCP no conectado","Apify scraping sin setup"]',
  '["Configurar Market Scanner","Conectar Supadata MCP","Primera análisis de oportunidades","Setup Apify scraping"]')
on conflict (id) do nothing;

insert into agents (id, name, description, project_id, schedule, trigger_id, enabled, runs_total, runs_success) values
('content-director-mp', 'Content Director MP', 'Genera piezas de contenido diario para Instagram/TikTok de Mente Pausada', 'mente-pausada', '07:00 ARG', 'trig_01Dzrvfv5cRPgpZqZECKTMdQ', false, 47, 45),
('polt-contenido', 'Polt Contenido Diario', 'Posts de Instagram y templates WhatsApp para Polt Mobilier', 'polt-mobilier', '09:00 ARG', 'trig_01Ejb3VtrRZB16cEQsaHsD7t', false, 31, 29),
('cerebro-scanner', 'Cerebro Market Scanner', 'Analiza tendencias y oportunidades de mercado cada lunes', 'cerebro', 'Lunes 09:00 ARG', 'trig_0137Yso9ckqHFFpgC2sGVAnJ', false, 8, 8),
('daily-digest', 'Daily Digest', 'Email matutino con top 3 acciones del día para los 3 proyectos', null, '08:00 ARG', 'trig_015iu2VG92yiAu36MWdargm6', false, 52, 51),
('daily-analytics', 'Daily Analytics', 'Reporte KPIs y tendencias de los 3 proyectos a las 5 PM', null, '17:00 ARG', 'trig_01UgD4bxJwaL7xBoSZixYunh', false, 52, 52),
('mp-scout', 'Scout Agent MP', 'Busca tendencias de contenido y competidores en bienestar/mindfulness', 'mente-pausada', 'Manual', null, true, 15, 13),
('polt-leads', 'Polt Lead Scorer', 'Califica y prioriza leads entrantes de WhatsApp y formularios web', 'polt-mobilier', 'Automático', null, true, 23, 21),
('self-improver', 'Self-Improver Loop', 'Revisa performance semanal de agentes y propone mejoras a prompts', null, 'Viernes 18:00 ARG', null, false, 3, 3)
on conflict (id) do nothing;

insert into system_state (id, active_projects, integrations) values
('global', '{"mente-pausada","polt-mobilier","cerebro"}', '{"sendgrid":"configured","hotmart":"pending","whapi":"pending","supadata":"pending","apify":"pending"}')
on conflict (id) do nothing;

export interface Client {
  id: number;
  name: string;
  industry: string | null;
  website: string | null;
  brand_voice: string | null;
  target_audience: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Project {
  id: number;
  client_id: number;
  name: string;
  description: string | null;
  status: string;
  goals: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Campaign {
  id: number;
  project_id: number;
  name: string;
  campaign_type: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  target_channels: string | null;
  strategy_brief: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Content {
  id: number;
  campaign_id: number | null;
  project_id: number;
  content_type: string | null;
  title: string | null;
  body: string | null;
  platform: string | null;
  status: string;
  seo_score: number | null;
  seo_suggestions: string | null;
  review_notes: string | null;
  agent_id: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Task {
  id: number;
  project_id: number | null;
  campaign_id: number | null;
  agent_type: string;
  task_type: string;
  input_data: string | null;
  output_data: string | null;
  status: string;
  priority: number;
  parent_task_id: number | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface AgentStatus {
  agent_type: string;
  display_name: string;
  description: string;
  status: string;
  tasks_completed: number;
  tasks_running: number;
}

export interface AgentLog {
  id: number;
  task_id: number;
  agent_type: string | null;
  log_level: string | null;
  message: string | null;
  created_at: string;
}

export interface AnalyticsOverview {
  total_clients: number;
  total_projects: number;
  total_campaigns: number;
  total_content: number;
  tasks_by_status: Record<string, number>;
  content_by_status: Record<string, number>;
}

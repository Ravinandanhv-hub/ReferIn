export interface Job {
  id: string;
  title: string;
  company: string;
  location: string | null;
  type: string;
  skills_required: string[];
  is_remote: boolean;
  experience_min: number;
  experience_max: number;
  posted_at: string;
  source: string | null;
}

export interface JobDetail extends Job {
  description: string | null;
  apply_url: string | null;
  created_at: string;
}

export interface JobListResponse {
  items: Job[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface RecommendedJob extends Job {
  score: number;
  match_reasons: string[];
}

export interface JobSearchParams {
  q?: string;
  location?: string;
  type?: string;
  is_remote?: boolean;
  experience_min?: number;
  experience_max?: number;
  page?: number;
  size?: number;
}

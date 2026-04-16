export interface User {
  id: string;
  name: string;
  email: string;
  role: "job_seeker" | "referrer" | "admin";
  skills: string[];
  experience: number;
  resume_url: string | null;
  location: string | null;
  preferences: UserPreferences;
  created_at: string;
}

export interface UserPreferences {
  job_type?: string[];
  locations?: string[];
}

export interface UserPublic {
  id: string;
  name: string;
  role: string;
  skills: string[];
  experience: number;
  location: string | null;
}

export interface UserUpdate {
  name?: string;
  skills?: string[];
  experience?: number;
  location?: string;
  resume_url?: string;
  preferences?: UserPreferences;
}

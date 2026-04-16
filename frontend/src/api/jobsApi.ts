import client from "./client";
import type {
  JobDetail,
  JobListResponse,
  RecommendedJob,
  JobSearchParams,
} from "../types/job";

export const jobsApi = {
  getJobs: (params: JobSearchParams = {}) =>
    client.get<JobListResponse>("/jobs", { params }),

  getJob: (id: string) => client.get<JobDetail>(`/jobs/${id}`),

  getRecommendedJobs: (limit: number = 10) =>
    client.get<{ items: RecommendedJob[] }>("/jobs/recommended", {
      params: { limit },
    }),
};

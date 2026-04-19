import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { jobsApi } from "../api/jobsApi";
import type {
  Job,
  JobDetail,
  RecommendedJob,
  JobSearchParams,
} from "../types/job";

interface JobsState {
  jobs: Job[];
  currentJob: JobDetail | null;
  recommendedJobs: RecommendedJob[];
  total: number;
  page: number;
  pages: number;
  loading: boolean;
  error: string | null;
  filters: JobSearchParams;
}

const initialState: JobsState = {
  jobs: [],
  currentJob: null,
  recommendedJobs: [],
  total: 0,
  page: 1,
  pages: 0,
  loading: false,
  error: null,
  filters: { page: 1, size: 20 },
};

export const fetchJobs = createAsyncThunk(
  "jobs/fetchJobs",
  async (params: JobSearchParams, { rejectWithValue }) => {
    try {
      const response = await jobsApi.getJobs(params);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to fetch jobs",
      );
    }
  },
);

export const fetchJob = createAsyncThunk(
  "jobs/fetchJob",
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await jobsApi.getJob(id);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to fetch job",
      );
    }
  },
);

export const fetchRecommendedJobs = createAsyncThunk(
  "jobs/fetchRecommended",
  async (limit: number = 10, { rejectWithValue }) => {
    try {
      const response = await jobsApi.getRecommendedJobs(limit);
      return response.data.items;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to fetch recommendations",
      );
    }
  },
);

const jobsSlice = createSlice({
  name: "jobs",
  initialState,
  reducers: {
    setFilters(state, action) {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters(state) {
      state.filters = { page: 1, size: 20 };
    },
    clearCurrentJob(state) {
      state.currentJob = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchJobs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJobs.fulfilled, (state, action) => {
        state.loading = false;
        state.jobs = action.payload.items;
        state.total = action.payload.total;
        state.page = action.payload.page;
        state.pages = action.payload.pages;
      })
      .addCase(fetchJobs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJob.fulfilled, (state, action) => {
        state.loading = false;
        state.currentJob = action.payload;
      })
      .addCase(fetchJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchRecommendedJobs.fulfilled, (state, action) => {
        state.recommendedJobs = action.payload;
      });
  },
});

export const { setFilters, clearFilters, clearCurrentJob } = jobsSlice.actions;
export default jobsSlice.reducer;

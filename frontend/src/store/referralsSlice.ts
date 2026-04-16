import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { referralsApi } from "../api/referralsApi";
import type { Referral, ReferralCreate } from "../types/referral";

interface ReferralsState {
  sent: Referral[];
  received: Referral[];
  loading: boolean;
  error: string | null;
}

const initialState: ReferralsState = {
  sent: [],
  received: [],
  loading: false,
  error: null,
};

export const fetchMyReferrals = createAsyncThunk(
  "referrals/fetchMy",
  async (status: string | undefined, { rejectWithValue }) => {
    try {
      const response = await referralsApi.getMyReferrals(status);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to fetch referrals",
      );
    }
  },
);

export const createReferral = createAsyncThunk(
  "referrals/create",
  async (data: ReferralCreate, { rejectWithValue }) => {
    try {
      const response = await referralsApi.createReferral(data);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to create referral",
      );
    }
  },
);

export const updateReferralStatus = createAsyncThunk(
  "referrals/updateStatus",
  async (
    { id, status }: { id: string; status: "accepted" | "rejected" },
    { rejectWithValue },
  ) => {
    try {
      const response = await referralsApi.updateReferral(id, status);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to update referral",
      );
    }
  },
);

const referralsSlice = createSlice({
  name: "referrals",
  initialState,
  reducers: {
    clearReferralError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMyReferrals.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMyReferrals.fulfilled, (state, action) => {
        state.loading = false;
        state.sent = action.payload.sent;
        state.received = action.payload.received;
      })
      .addCase(fetchMyReferrals.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createReferral.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createReferral.fulfilled, (state, action) => {
        state.loading = false;
        state.sent.unshift(action.payload);
      })
      .addCase(createReferral.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateReferralStatus.fulfilled, (state, action) => {
        const updated = action.payload;
        const idx = state.received.findIndex((r) => r.id === updated.id);
        if (idx !== -1) {
          state.received[idx] = updated;
        }
      });
  },
});

export const { clearReferralError } = referralsSlice.actions;
export default referralsSlice.reducer;

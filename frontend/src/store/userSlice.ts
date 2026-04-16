import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { usersApi } from "../api/usersApi";
import type { User, UserUpdate } from "../types/user";
import type { Notification } from "../types/api";

interface UserState {
  notifications: Notification[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  notifications: [],
  loading: false,
  error: null,
};

export const updateProfile = createAsyncThunk(
  "user/updateProfile",
  async (data: UserUpdate, { rejectWithValue }) => {
    try {
      const response = await usersApi.updateProfile(data);
      return response.data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to update profile",
      );
    }
  },
);

export const fetchNotifications = createAsyncThunk(
  "user/fetchNotifications",
  async (unreadOnly: boolean = false, { rejectWithValue }) => {
    try {
      const response = await usersApi.getNotifications(unreadOnly);
      return response.data.items;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.detail || "Failed to fetch notifications",
      );
    }
  },
);

export const markNotificationRead = createAsyncThunk(
  "user/markNotificationRead",
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await usersApi.markNotificationRead(id);
      return response.data;
    } catch (err: any) {
      return rejectWithValue("Failed to mark notification as read");
    }
  },
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotifications.fulfilled, (state, action) => {
        state.notifications = action.payload;
      })
      .addCase(markNotificationRead.fulfilled, (state, action) => {
        const idx = state.notifications.findIndex(
          (n) => n.id === action.payload.id,
        );
        if (idx !== -1) {
          state.notifications[idx] = action.payload;
        }
      });
  },
});

export default userSlice.reducer;

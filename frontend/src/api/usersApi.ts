import client from "./client";
import type { User, UserPublic, UserUpdate } from "../types/user";
import type { Notification } from "../types/api";

export const usersApi = {
  getUser: (id: string) => client.get<UserPublic>(`/users/${id}`),

  updateProfile: (data: UserUpdate) => client.put<User>("/users/profile", data),

  getNotifications: (unreadOnly: boolean = false) =>
    client.get<{ items: Notification[] }>("/notifications", {
      params: { unread_only: unreadOnly },
    }),

  markNotificationRead: (id: string) =>
    client.patch<Notification>(`/notifications/${id}/read`),
};

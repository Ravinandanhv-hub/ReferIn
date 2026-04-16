import client from "./client";
import type { User } from "../types/user";

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  role: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  register: (data: RegisterRequest) =>
    client.post<User>("/auth/register", data),

  login: (data: LoginRequest) =>
    client.post<TokenResponse>("/auth/login", data),

  getMe: () => client.get<User>("/auth/me"),
};

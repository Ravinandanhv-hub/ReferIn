import client from "./client";
import type {
  Referral,
  ReferralCreate,
  ReferralListResponse,
} from "../types/referral";

export const referralsApi = {
  createReferral: (data: ReferralCreate) =>
    client.post<Referral>("/referrals", data),

  getMyReferrals: (status?: string) =>
    client.get<ReferralListResponse>("/referrals/my", {
      params: status ? { status } : {},
    }),

  updateReferral: (id: string, status: "accepted" | "rejected") =>
    client.patch<Referral>(`/referrals/${id}`, { status }),
};

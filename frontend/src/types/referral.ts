export interface Referral {
  id: string;
  job_id: string;
  requester_id: string;
  referrer_id: string;
  status: "pending" | "accepted" | "rejected";
  message: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReferralCreate {
  job_id: string;
  referrer_id: string;
  message?: string;
}

export interface ReferralListResponse {
  sent: Referral[];
  received: Referral[];
}

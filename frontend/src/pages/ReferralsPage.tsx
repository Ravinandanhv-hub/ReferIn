import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/useAppStore';
import { fetchMyReferrals, updateReferralStatus } from '../store/referralsSlice';

const STATUS_STYLES: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-700',
  accepted: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
};

export default function ReferralsPage() {
  const dispatch = useAppDispatch();
  const { sent, received, loading, error } = useAppSelector((s) => s.referrals);
  const [tab, setTab] = useState<'sent' | 'received'>('sent');

  useEffect(() => {
    dispatch(fetchMyReferrals(undefined));
  }, [dispatch]);

  const handleUpdateStatus = (id: string, status: 'accepted' | 'rejected') => {
    dispatch(updateReferralStatus({ id, status }));
  };

  const referrals = tab === 'sent' ? sent : received;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Referrals</h1>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-gray-100 rounded-lg p-1 w-fit">
        <button
          onClick={() => setTab('sent')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            tab === 'sent' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Sent ({sent.length})
        </button>
        <button
          onClick={() => setTab('received')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            tab === 'received'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Received ({received.length})
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>
      ) : referrals.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
          <p className="text-gray-500">
            {tab === 'sent'
              ? "You haven't sent any referral requests yet"
              : "You haven't received any referral requests yet"}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {referrals.map((referral) => (
            <div
              key={referral.id}
              className="bg-white rounded-xl border border-gray-200 p-5"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        STATUS_STYLES[referral.status]
                      }`}
                    >
                      {referral.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    Job ID: <span className="font-mono text-xs">{referral.job_id}</span>
                  </p>
                  {tab === 'sent' && (
                    <p className="text-sm text-gray-600">
                      Referrer: <span className="font-mono text-xs">{referral.referrer_id}</span>
                    </p>
                  )}
                  {tab === 'received' && (
                    <p className="text-sm text-gray-600">
                      From: <span className="font-mono text-xs">{referral.requester_id}</span>
                    </p>
                  )}
                  {referral.message && (
                    <p className="text-sm text-gray-500 mt-2 italic">"{referral.message}"</p>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {tab === 'received' && referral.status === 'pending' && (
                    <>
                      <button
                        onClick={() => handleUpdateStatus(referral.id, 'accepted')}
                        className="text-xs bg-green-600 text-white px-3 py-1.5 rounded-lg hover:bg-green-700 font-medium"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(referral.id, 'rejected')}
                        className="text-xs bg-red-600 text-white px-3 py-1.5 rounded-lg hover:bg-red-700 font-medium"
                      >
                        Reject
                      </button>
                    </>
                  )}
                </div>
              </div>

              <p className="text-xs text-gray-400 mt-2">
                Created: {new Date(referral.created_at).toLocaleDateString()}
                {referral.updated_at !== referral.created_at && (
                  <> · Updated: {new Date(referral.updated_at).toLocaleDateString()}</>
                )}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

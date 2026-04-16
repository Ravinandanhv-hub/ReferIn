import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useAppStore';
import { fetchJob, clearCurrentJob } from '../store/jobsSlice';
import { createReferral, clearReferralError } from '../store/referralsSlice';

const TYPE_LABELS: Record<string, string> = {
  full_time: 'Full-time',
  part_time: 'Part-time',
  contract: 'Contract',
  internship: 'Internship',
};

export default function JobDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const dispatch = useAppDispatch();
  const { currentJob, loading } = useAppSelector((s) => s.jobs);
  const { user } = useAppSelector((s) => s.auth);
  const { error: referralError } = useAppSelector((s) => s.referrals);

  const [showReferralModal, setShowReferralModal] = useState(false);
  const [referrerId, setReferrerId] = useState('');
  const [message, setMessage] = useState('');
  const [referralSent, setReferralSent] = useState(false);

  useEffect(() => {
    if (id) dispatch(fetchJob(id));
    return () => { dispatch(clearCurrentJob()); };
  }, [id, dispatch]);

  const handleRequestReferral = async () => {
    if (!id || !referrerId) return;
    dispatch(clearReferralError());
    const result = await dispatch(
      createReferral({ job_id: id, referrer_id: referrerId, message: message || undefined })
    );
    if (createReferral.fulfilled.match(result)) {
      setShowReferralModal(false);
      setReferralSent(true);
      setReferrerId('');
      setMessage('');
    }
  };

  if (loading || !currentJob) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <Link to="/jobs" className="text-indigo-600 hover:text-indigo-700 text-sm font-medium mb-4 inline-block">
        ← Back to Jobs
      </Link>

      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{currentJob.title}</h1>
            <p className="text-lg text-gray-700 font-medium mt-1">{currentJob.company}</p>
          </div>
          <span className="text-sm bg-gray-100 text-gray-600 px-3 py-1 rounded-full">
            {TYPE_LABELS[currentJob.type] || currentJob.type}
          </span>
        </div>

        <div className="flex flex-wrap gap-3 text-sm text-gray-500 mb-6">
          <span>📍 {currentJob.location || 'Not specified'}</span>
          {currentJob.is_remote && <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded">Remote</span>}
          <span>💼 {currentJob.experience_min}-{currentJob.experience_max} years</span>
          {currentJob.source && <span>🔗 via {currentJob.source}</span>}
          <span>📅 Posted {new Date(currentJob.posted_at).toLocaleDateString()}</span>
        </div>

        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Skills Required</h2>
          <div className="flex flex-wrap gap-2">
            {currentJob.skills_required.map((skill) => (
              <span key={skill} className="bg-indigo-50 text-indigo-600 px-3 py-1 rounded-lg text-sm font-medium">
                {skill}
              </span>
            ))}
          </div>
        </div>

        {currentJob.description && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Description</h2>
            <p className="text-gray-600 leading-relaxed whitespace-pre-wrap">{currentJob.description}</p>
          </div>
        )}

        <div className="flex gap-3 pt-6 border-t border-gray-200">
          {currentJob.apply_url && (
            <a
              href={currentJob.apply_url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg hover:bg-indigo-700 font-medium"
            >
              Apply Now
            </a>
          )}
          {user && !referralSent && (
            <button
              onClick={() => setShowReferralModal(true)}
              className="border border-indigo-600 text-indigo-600 px-6 py-2.5 rounded-lg hover:bg-indigo-50 font-medium"
            >
              Request Referral
            </button>
          )}
          {referralSent && (
            <span className="text-green-600 font-medium py-2.5">✓ Referral request sent!</span>
          )}
        </div>
      </div>

      {/* Referral Modal */}
      {showReferralModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Request Referral</h2>

            {referralError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {referralError}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Referrer ID
                </label>
                <input
                  type="text"
                  value={referrerId}
                  onChange={(e) => setReferrerId(e.target.value)}
                  placeholder="Enter referrer's user ID"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                />
                <p className="text-xs text-gray-400 mt-1">Ask the referrer for their profile ID</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Message (optional)
                </label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={3}
                  placeholder="Why should they refer you?"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleRequestReferral}
                disabled={!referrerId}
                className="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 font-medium disabled:opacity-50"
              >
                Send Request
              </button>
              <button
                onClick={() => setShowReferralModal(false)}
                className="flex-1 border border-gray-300 py-2 rounded-lg hover:bg-gray-50 font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

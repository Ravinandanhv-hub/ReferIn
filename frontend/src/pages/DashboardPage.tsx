import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useAppStore';
import { fetchRecommendedJobs } from '../store/jobsSlice';
import { fetchMyReferrals } from '../store/referralsSlice';
import { fetchNotifications } from '../store/userSlice';

export default function DashboardPage() {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((s) => s.auth);
  const { recommendedJobs } = useAppSelector((s) => s.jobs);
  const { sent, received } = useAppSelector((s) => s.referrals);
  const { notifications } = useAppSelector((s) => s.user);

  useEffect(() => {
    dispatch(fetchRecommendedJobs(6));
    dispatch(fetchMyReferrals(undefined));
    dispatch(fetchNotifications(false));
  }, [dispatch]);

  const pendingSent = sent.filter((r) => r.status === 'pending').length;
  const pendingReceived = received.filter((r) => r.status === 'pending').length;
  const unread = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.name}!
        </h1>
        <p className="text-gray-500 mt-1">Here's your activity overview</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm text-gray-500">Referrals Sent</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{sent.length}</p>
          <p className="text-xs text-yellow-600 mt-1">{pendingSent} pending</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm text-gray-500">Referrals Received</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{received.length}</p>
          <p className="text-xs text-yellow-600 mt-1">{pendingReceived} pending</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm text-gray-500">Recommendations</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{recommendedJobs.length}</p>
          <p className="text-xs text-green-600 mt-1">personalized for you</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm text-gray-500">Notifications</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{notifications.length}</p>
          <p className="text-xs text-blue-600 mt-1">{unread} unread</p>
        </div>
      </div>

      {/* Recommended Jobs */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recommended Jobs</h2>
          <Link to="/jobs" className="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
            View all jobs →
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {recommendedJobs.slice(0, 6).map((job) => (
            <Link
              key={job.id}
              to={`/jobs/${job.id}`}
              className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-medium text-gray-900 line-clamp-1">{job.title}</h3>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full whitespace-nowrap ml-2">
                  {Math.round(job.score * 100)}% match
                </span>
              </div>
              <p className="text-sm text-gray-600">{job.company}</p>
              <p className="text-xs text-gray-400 mt-1">{job.location || 'Remote'}</p>
              <div className="flex flex-wrap gap-1 mt-3">
                {job.skills_required.slice(0, 3).map((skill) => (
                  <span key={skill} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded">
                    {skill}
                  </span>
                ))}
              </div>
              {job.match_reasons.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {job.match_reasons.slice(0, 2).map((reason, i) => (
                    <span key={i} className="text-xs text-gray-400">• {reason}</span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Notifications */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Notifications</h2>
        <div className="bg-white rounded-xl border border-gray-200 divide-y divide-gray-100">
          {notifications.length === 0 ? (
            <div className="p-6 text-center text-gray-400">No notifications yet</div>
          ) : (
            notifications.slice(0, 5).map((notif) => (
              <div key={notif.id} className={`p-4 ${!notif.is_read ? 'bg-indigo-50/50' : ''}`}>
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{notif.title}</p>
                    <p className="text-sm text-gray-500 mt-0.5">{notif.message}</p>
                  </div>
                  {!notif.is_read && (
                    <span className="w-2 h-2 bg-indigo-600 rounded-full flex-shrink-0 mt-2"></span>
                  )}
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {new Date(notif.created_at).toLocaleDateString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

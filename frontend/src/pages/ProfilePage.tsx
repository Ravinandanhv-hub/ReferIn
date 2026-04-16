import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/useAppStore';
import { updateProfile } from '../store/userSlice';
import { loadUser } from '../store/authSlice';

export default function ProfilePage() {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((s) => s.auth);

  const [form, setForm] = useState({
    name: user?.name || '',
    skills: user?.skills?.join(', ') || '',
    experience: user?.experience || 0,
    location: user?.location || '',
    resume_url: user?.resume_url || '',
    pref_job_type: user?.preferences?.job_type?.join(', ') || '',
    pref_locations: user?.preferences?.locations?.join(', ') || '',
  });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSaved(false);

    const skills = form.skills
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const prefJobType = form.pref_job_type
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const prefLocations = form.pref_locations
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);

    const result = await dispatch(
      updateProfile({
        name: form.name,
        skills,
        experience: form.experience,
        location: form.location || undefined,
        resume_url: form.resume_url || undefined,
        preferences: {
          job_type: prefJobType.length > 0 ? prefJobType : undefined,
          locations: prefLocations.length > 0 ? prefLocations : undefined,
        },
      })
    );

    setSaving(false);
    if (updateProfile.fulfilled.match(result)) {
      setSaved(true);
      dispatch(loadUser());
      setTimeout(() => setSaved(false), 3000);
    } else {
      setError((result.payload as string) || 'Failed to update profile');
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">My Profile</h1>
      <p className="text-gray-500 mb-6">
        <span className="capitalize">{user.role.replace('_', ' ')}</span> · Member since{' '}
        {new Date(user.created_at).toLocaleDateString()}
      </p>

      {/* Profile ID */}
      <div className="bg-indigo-50 rounded-lg p-4 mb-6">
        <p className="text-sm text-indigo-600">
          <strong>Your Profile ID:</strong>{' '}
          <code className="text-xs bg-indigo-100 px-2 py-0.5 rounded">{user.id}</code>
        </p>
        <p className="text-xs text-indigo-400 mt-1">Share this with others so they can send you referral requests</p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">{error}</div>
      )}
      {saved && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          Profile updated successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input
            type="text"
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            type="email"
            disabled
            value={user.email}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-gray-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Skills (comma-separated)</label>
          <input
            type="text"
            value={form.skills}
            onChange={(e) => setForm({ ...form, skills: e.target.value })}
            placeholder="React, TypeScript, Python..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Years of Experience</label>
          <input
            type="number"
            min={0}
            value={form.experience}
            onChange={(e) => setForm({ ...form, experience: parseInt(e.target.value) || 0 })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
          <input
            type="text"
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            placeholder="City, Country"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Resume URL</label>
          <input
            type="url"
            value={form.resume_url}
            onChange={(e) => setForm({ ...form, resume_url: e.target.value })}
            placeholder="https://..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <hr className="border-gray-200" />

        <h3 className="text-sm font-semibold text-gray-700">Preferences</h3>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Preferred Job Types (comma-separated)
          </label>
          <input
            type="text"
            value={form.pref_job_type}
            onChange={(e) => setForm({ ...form, pref_job_type: e.target.value })}
            placeholder="full_time, remote, contract..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Preferred Locations (comma-separated)
          </label>
          <input
            type="text"
            value={form.pref_locations}
            onChange={(e) => setForm({ ...form, pref_locations: e.target.value })}
            placeholder="India, US, UK..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full bg-indigo-600 text-white py-2.5 rounded-lg hover:bg-indigo-700 font-medium disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </form>
    </div>
  );
}

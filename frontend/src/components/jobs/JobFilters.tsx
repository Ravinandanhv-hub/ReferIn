import type { JobSearchParams } from '../../types/job';

interface Props {
  filters: JobSearchParams;
  onChange: (filters: JobSearchParams) => void;
  onReset: () => void;
}

export default function JobFilters({ filters, onChange, onReset }: Props) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-gray-900">Filters</h3>
        <button onClick={onReset} className="text-xs text-indigo-600 hover:text-indigo-700">
          Reset
        </button>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
        <input
          type="text"
          value={filters.q || ''}
          onChange={(e) => onChange({ ...filters, q: e.target.value || undefined, page: 1 })}
          placeholder="Job title, skill, company..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
        <input
          type="text"
          value={filters.location || ''}
          onChange={(e) => onChange({ ...filters, location: e.target.value || undefined, page: 1 })}
          placeholder="City, country..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Job Type</label>
        <select
          value={filters.type || ''}
          onChange={(e) => onChange({ ...filters, type: e.target.value || undefined, page: 1 })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        >
          <option value="">All Types</option>
          <option value="full_time">Full-time</option>
          <option value="part_time">Part-time</option>
          <option value="contract">Contract</option>
          <option value="internship">Internship</option>
        </select>
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="remote"
          checked={filters.is_remote || false}
          onChange={(e) =>
            onChange({ ...filters, is_remote: e.target.checked || undefined, page: 1 })
          }
          className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
        <label htmlFor="remote" className="text-sm text-gray-700">
          Remote only
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Experience (years)</label>
        <div className="flex gap-2">
          <input
            type="number"
            min={0}
            value={filters.experience_min ?? ''}
            onChange={(e) =>
              onChange({
                ...filters,
                experience_min: e.target.value ? parseInt(e.target.value) : undefined,
                page: 1,
              })
            }
            placeholder="Min"
            className="w-1/2 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
          <input
            type="number"
            min={0}
            value={filters.experience_max ?? ''}
            onChange={(e) =>
              onChange({
                ...filters,
                experience_max: e.target.value ? parseInt(e.target.value) : undefined,
                page: 1,
              })
            }
            placeholder="Max"
            className="w-1/2 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>
      </div>
    </div>
  );
}

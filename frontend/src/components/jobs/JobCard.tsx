import { Link } from 'react-router-dom';
import type { Job } from '../../types/job';

const TYPE_LABELS: Record<string, string> = {
  full_time: 'Full-time',
  part_time: 'Part-time',
  contract: 'Contract',
  internship: 'Internship',
};

export default function JobCard({ job }: { job: Job }) {
  const postedDate = new Date(job.posted_at);
  const daysAgo = Math.floor((Date.now() - postedDate.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <Link
      to={`/jobs/${job.id}`}
      className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow block"
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-gray-900 line-clamp-1">{job.title}</h3>
        <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full whitespace-nowrap ml-2">
          {TYPE_LABELS[job.type] || job.type}
        </span>
      </div>

      <p className="text-sm text-gray-700 font-medium">{job.company}</p>

      <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
        <span>{job.location || 'Location not specified'}</span>
        {job.is_remote && (
          <span className="bg-green-100 text-green-700 px-1.5 py-0.5 rounded">Remote</span>
        )}
        <span>
          {job.experience_min}-{job.experience_max} yrs
        </span>
      </div>

      <div className="flex flex-wrap gap-1.5 mt-3">
        {job.skills_required.slice(0, 4).map((skill) => (
          <span key={skill} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded">
            {skill}
          </span>
        ))}
        {job.skills_required.length > 4 && (
          <span className="text-xs text-gray-400">+{job.skills_required.length - 4} more</span>
        )}
      </div>

      <div className="flex justify-between items-center mt-3 pt-3 border-t border-gray-100">
        <span className="text-xs text-gray-400">
          {daysAgo === 0 ? 'Today' : `${daysAgo}d ago`}
        </span>
        {job.source && <span className="text-xs text-gray-400">via {job.source}</span>}
      </div>
    </Link>
  );
}

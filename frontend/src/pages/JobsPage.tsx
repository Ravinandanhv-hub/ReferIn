import { useEffect, useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/useAppStore';
import { fetchJobs, setFilters, clearFilters } from '../store/jobsSlice';
import JobCard from '../components/jobs/JobCard';
import JobFilters from '../components/jobs/JobFilters';
import type { JobSearchParams } from '../types/job';

export default function JobsPage() {
  const dispatch = useAppDispatch();
  const { jobs, total, page, pages, loading, filters } = useAppSelector((s) => s.jobs);

  const loadJobs = useCallback(
    (params: JobSearchParams) => {
      dispatch(fetchJobs(params));
    },
    [dispatch]
  );

  useEffect(() => {
    loadJobs(filters);
  }, [filters, loadJobs]);

  const handleFilterChange = (newFilters: JobSearchParams) => {
    dispatch(setFilters(newFilters));
  };

  const handleReset = () => {
    dispatch(clearFilters());
  };

  const handlePageChange = (newPage: number) => {
    dispatch(setFilters({ ...filters, page: newPage }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Browse Jobs</h1>
        <p className="text-gray-500 mt-1">{total} jobs found</p>
      </div>

      <div className="flex gap-6">
        {/* Filters Sidebar */}
        <div className="w-72 flex-shrink-0 hidden lg:block">
          <JobFilters filters={filters} onChange={handleFilterChange} onReset={handleReset} />
        </div>

        {/* Job Listings */}
        <div className="flex-1">
          {loading ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
          ) : jobs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No jobs found matching your criteria</p>
              <button
                onClick={handleReset}
                className="mt-3 text-indigo-600 hover:text-indigo-700 text-sm font-medium"
              >
                Clear filters
              </button>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {jobs.map((job) => (
                  <JobCard key={job.id} job={job} />
                ))}
              </div>

              {/* Pagination */}
              {pages > 1 && (
                <div className="flex justify-center items-center gap-2 mt-8">
                  <button
                    onClick={() => handlePageChange(page - 1)}
                    disabled={page <= 1}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm disabled:opacity-50 hover:bg-gray-50"
                  >
                    Previous
                  </button>
                  {Array.from({ length: Math.min(pages, 5) }, (_, i) => {
                    const pageNum = i + 1;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`px-3 py-1.5 rounded-lg text-sm ${
                          pageNum === page
                            ? 'bg-indigo-600 text-white'
                            : 'border border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  <button
                    onClick={() => handlePageChange(page + 1)}
                    disabled={page >= pages}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm disabled:opacity-50 hover:bg-gray-50"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

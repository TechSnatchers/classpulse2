import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { SearchIcon, CalendarIcon, ClockIcon, UsersIcon, ActivityIcon, PlayIcon, VideoIcon, TrendingUpIcon, BookOpenIcon, PlusIcon, EditIcon } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { sessionService, Session } from '../../services/sessionService';

export const SessionList = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');

  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';

  // Load sessions from service
  useEffect(() => {
    const loadSessions = () => {
      const allSessions = sessionService.getAllSessions();
      setSessions(allSessions);
    };

    loadSessions();
    
    // Reload sessions periodically to catch status updates
    const interval = setInterval(loadSessions, 30000); // Every 30 seconds
    
    // Listen for storage changes (when sessions are created/updated in other tabs)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'learning_platform_sessions') {
        loadSessions();
      }
    };
    window.addEventListener('storage', handleStorageChange);

    return () => {
      clearInterval(interval);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  // Filter sessions
  let filteredSessions = sessions.filter(session => {
    const matchesSearch = session.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      session.course.toLowerCase().includes(searchTerm.toLowerCase()) ||
      session.instructor.toLowerCase().includes(searchTerm.toLowerCase()) ||
      session.courseCode.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return false;
    
    if (statusFilter !== 'all' && session.status !== statusFilter) {
      return false;
    }
    
    return true;
  });

  // Sort sessions: live first, then upcoming, then completed
  filteredSessions = [...filteredSessions].sort((a, b) => {
    const statusOrder = { live: 0, upcoming: 1, completed: 2 };
    if (statusOrder[a.status as keyof typeof statusOrder] !== statusOrder[b.status as keyof typeof statusOrder]) {
      return statusOrder[a.status as keyof typeof statusOrder] - statusOrder[b.status as keyof typeof statusOrder];
    }
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'live':
        return <Badge variant="danger" className="bg-red-600 text-white">LIVE</Badge>;
      case 'upcoming':
        return <Badge variant="success">Upcoming</Badge>;
      case 'completed':
        return <Badge variant="default">Completed</Badge>;
      default:
        return null;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'live':
        return <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />;
      case 'upcoming':
        return <CalendarIcon className="h-4 w-4 text-green-600" />;
      case 'completed':
        return <VideoIcon className="h-4 w-4 text-gray-400" />;
      default:
        return null;
    }
  };

  return (
    <div className="py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Live Sessions</h1>
          <p className="mt-1 text-sm text-gray-500">
            View and join upcoming, live, and past sessions
          </p>
        </div>
        {isInstructor && (
          <Button
            variant="primary"
            leftIcon={<PlusIcon className="h-4 w-4" />}
            onClick={() => navigate('/dashboard/sessions/create')}
          >
            Create Session
          </Button>
        )}
      </div>

      {/* Search and Filter */}
      <Card className="mb-6">
        <div className="p-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="relative flex-1 max-w-md">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <SearchIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                placeholder="Search sessions..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <button
              type="button"
              onClick={() => setFilterActive(!filterActive)}
              className={`inline-flex items-center px-4 py-2 border rounded-md text-sm font-medium ${
                filterActive
                  ? 'border-indigo-600 text-indigo-600 bg-indigo-50'
                  : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            >
              <CalendarIcon className="-ml-1 mr-2 h-5 w-5" />
              Filters
              </button>
          </div>

          {/* Filter Options */}
          {filterActive && (
            <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  id="status"
                  value={statusFilter}
                  onChange={e => setStatusFilter(e.target.value)}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="all">All Sessions</option>
                  <option value="live">Live</option>
                  <option value="upcoming">Upcoming</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div>
                <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
                  Date Range
                </label>
                <select
                  id="date"
                  value={dateFilter}
                  onChange={e => setDateFilter(e.target.value)}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="all">All Dates</option>
                  <option value="today">Today</option>
                  <option value="week">This Week</option>
                  <option value="month">This Month</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  type="button"
                  onClick={() => {
                    setStatusFilter('all');
                    setDateFilter('all');
                    setSearchTerm('');
                  }}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Session Cards */}
      {filteredSessions.length === 0 ? (
        <Card className="p-12 text-center">
          <CalendarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No sessions found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Try adjusting your search or filter criteria.
          </p>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredSessions.map(session => (
            <Card
              key={session.id}
              className={`overflow-hidden transition-all hover:shadow-lg ${
                session.status === 'live' ? 'border-2 border-red-500' : ''
              }`}
            >
              <div className="p-6">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                  {/* Left Section - Session Info */}
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-xl font-semibold text-gray-900">
                          {session.title}
                          </h3>
                          {getStatusBadge(session.status)}
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                          <div className="flex items-center">
                            <BookOpenIcon className="h-4 w-4 mr-1" />
                            <span className="font-medium">{session.course}</span>
                            <span className="ml-2 text-gray-400">({session.courseCode})</span>
                          </div>
                        </div>
                        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                          <div className="flex items-center">
                            <UsersIcon className="h-4 w-4 mr-1" />
                            <span>{session.instructor}</span>
                          </div>
                          <div className="flex items-center">
                            <CalendarIcon className="h-4 w-4 mr-1" />
                            <span>{session.date}</span>
                          </div>
                          <div className="flex items-center">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            <span>{session.time}</span>
                            <span className="ml-1 text-gray-400">({session.duration})</span>
                          </div>
                          {session.status === 'live' && (
                            <div className="flex items-center">
                              {getStatusIcon(session.status)}
                              <span className="ml-2 font-medium text-red-600">
                                {session.participants} participants
                              </span>
                            </div>
                          )}
                          {session.status === 'upcoming' && (
                            <div className="flex items-center">
                              <UsersIcon className="h-4 w-4 mr-1" />
                              <span>
                                {session.expectedParticipants} expected
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Engagement Metrics */}
                    {session.engagement && (
                      <div className="mt-4 p-3 bg-indigo-50 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <ActivityIcon className="h-4 w-4 text-indigo-600" />
                            <span className="text-sm font-medium text-indigo-900">
                              Engagement: {session.engagement}%
                            </span>
                          </div>
                          <div className="w-32 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-indigo-600 h-2 rounded-full"
                              style={{ width: `${session.engagement}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Right Section - Actions */}
                  <div className="flex flex-col sm:flex-row gap-3 lg:flex-col lg:items-end">
                    {isInstructor && (
                      <Button
                        variant="outline"
                        size="sm"
                        leftIcon={<EditIcon className="h-4 w-4" />}
                        onClick={() => navigate(`/dashboard/sessions/${session.id}/edit`)}
                        className="w-full sm:w-auto"
                      >
                        Edit
                      </Button>
                    )}
                    {session.status === 'live' && (
                      <Link to={`/dashboard/sessions/${session.id}`} className="w-full sm:w-auto">
                        <Button
                          variant="primary"
                          leftIcon={<PlayIcon className="h-4 w-4" />}
                          className="w-full"
                        >
                          Join Live
                        </Button>
                      </Link>
                    )}
                    {session.status === 'upcoming' && (
                      <Link to={`/dashboard/sessions/${session.id}`} className="w-full sm:w-auto">
                        <Button
                          variant="outline"
                          leftIcon={<CalendarIcon className="h-4 w-4" />}
                          className="w-full"
                        >
                          View Details
                        </Button>
                      </Link>
                    )}
                    {session.status === 'completed' && (
                      <>
                        <Link to={`/dashboard/sessions/${session.id}`} className="w-full sm:w-auto">
                          <Button
                            variant="outline"
                            leftIcon={<VideoIcon className="h-4 w-4" />}
                            className="w-full"
                          >
                            {session.recordingAvailable ? 'Watch Recording' : 'View Details'}
                          </Button>
                        </Link>
                        {session.engagement && (
                          <div className="text-center lg:text-right">
                            <p className="text-xs text-gray-500">Your Engagement</p>
                            <p className="text-lg font-semibold text-gray-900">
                              {session.engagement}%
                            </p>
                          </div>
                        )}
                      </>
                    )}
                      </div>
                      </div>
          </div>
            </Card>
          ))}
        </div>
      )}

      {/* Summary Stats */}
      {user?.role === 'instructor' || user?.role === 'admin' ? (
        <Card className="mt-6">
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Session Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-red-600">
                  {sessions.filter(s => s.status === 'live').length}
                </p>
                <p className="text-sm text-gray-600">Live Now</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">
                  {sessions.filter(s => s.status === 'upcoming').length}
                </p>
                <p className="text-sm text-gray-600">Upcoming</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-600">
                  {sessions.filter(s => s.status === 'completed').length}
                </p>
                <p className="text-sm text-gray-600">Completed</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-indigo-600">
                  {Math.round(
                    sessions
                      .filter(s => s.engagement)
                      .reduce((sum, s) => sum + (s.engagement || 0), 0) /
                      sessions.filter(s => s.engagement).length
                  ) || 0}%
                </p>
                <p className="text-sm text-gray-600">Avg Engagement</p>
              </div>
            </div>
          </div>
        </Card>
      ) : null}
      </div>
  );
};

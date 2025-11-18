import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { SearchIcon, FilterIcon, BookOpenIcon, UsersIcon, CalendarIcon, TrendingUpIcon, ActivityIcon, ClockIcon } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { EngagementIndicator } from '../../components/engagement/EngagementIndicator';

// Mock course data with engagement metrics
const courses = [
  {
  id: '1',
  title: 'Machine Learning Fundamentals',
  code: 'CS301',
  instructor: 'Dr. Jane Smith',
  students: 45,
  sessions: 12,
    completedSessions: 8,
    lastActive: '2023-10-10',
    engagement: 85,
    engagementLevel: 'high' as const,
    progress: 67,
    upcomingSession: '2023-10-15',
    color: 'bg-gradient-to-br from-indigo-500 to-purple-600'
  },
  {
  id: '2',
  title: 'Database Systems',
  code: 'CS202',
  instructor: 'Prof. John Doe',
  students: 38,
  sessions: 10,
    completedSessions: 6,
    lastActive: '2023-10-09',
    engagement: 72,
    engagementLevel: 'medium' as const,
    progress: 60,
    upcomingSession: '2023-10-16',
    color: 'bg-gradient-to-br from-blue-500 to-cyan-600'
  },
  {
  id: '3',
  title: 'Advanced Programming Techniques',
  code: 'CS304',
  instructor: 'Dr. Maria Rodriguez',
  students: 30,
  sessions: 8,
    completedSessions: 5,
    lastActive: '2023-10-11',
    engagement: 78,
    engagementLevel: 'high' as const,
    progress: 62,
    upcomingSession: '2023-10-18',
    color: 'bg-gradient-to-br from-green-500 to-emerald-600'
  },
  {
  id: '4',
  title: 'Data Structures and Algorithms',
  code: 'CS201',
  instructor: 'Prof. David Chen',
  students: 42,
  sessions: 14,
    completedSessions: 10,
    lastActive: '2023-10-08',
    engagement: 65,
    engagementLevel: 'medium' as const,
    progress: 71,
    upcomingSession: '2023-10-12',
    color: 'bg-gradient-to-br from-orange-500 to-red-600'
  },
  {
  id: '5',
  title: 'Web Development',
  code: 'CS305',
  instructor: 'Dr. Alex Johnson',
  students: 35,
  sessions: 10,
    completedSessions: 7,
    lastActive: '2023-10-07',
    engagement: 80,
    engagementLevel: 'high' as const,
    progress: 70,
    upcomingSession: '2023-10-14',
    color: 'bg-gradient-to-br from-pink-500 to-rose-600'
  }
];

export const CourseList = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('recent');

  // Filter and sort courses
  let filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return false;
    
    if (statusFilter === 'active') {
      return course.completedSessions < course.sessions;
    } else if (statusFilter === 'completed') {
      return course.completedSessions === course.sessions;
    }
    
    return true;
  });

  // Sort courses
  filteredCourses = [...filteredCourses].sort((a, b) => {
    switch (sortBy) {
      case 'title':
        return a.title.localeCompare(b.title);
      case 'code':
        return a.code.localeCompare(b.code);
      case 'engagement':
        return b.engagement - a.engagement;
      case 'progress':
        return b.progress - a.progress;
      case 'recent':
      default:
        return new Date(b.lastActive).getTime() - new Date(a.lastActive).getTime();
    }
  });

  return (
    <div className="py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">My Courses</h1>
          <p className="mt-1 text-sm text-gray-500">
            {user?.role === 'instructor' ? 'Courses you are teaching' : 'Courses you are enrolled in'}
          </p>
        </div>
        {user?.role === 'instructor' || user?.role === 'admin' ? (
          <button
            onClick={() => navigate('/dashboard/courses/create')}
            className="mt-4 sm:mt-0 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Create New Course
          </button>
        ) : null}
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
                placeholder="Search courses..."
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
              <FilterIcon className="-ml-1 mr-2 h-5 w-5" />
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
                  <option value="all">All Courses</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div>
                <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
                  Sort By
                </label>
                <select
                  id="sort"
                  value={sortBy}
                  onChange={e => setSortBy(e.target.value)}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="recent">Most Recent</option>
                  <option value="title">Title</option>
                  <option value="code">Course Code</option>
                  <option value="engagement">Engagement</option>
                  <option value="progress">Progress</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  type="button"
                  onClick={() => {
                    setStatusFilter('all');
                    setSortBy('recent');
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

      {/* Course Grid */}
      {filteredCourses.length === 0 ? (
        <Card className="p-12 text-center">
          <BookOpenIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No courses found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Try adjusting your search or filter criteria.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map(course => (
            <Card key={course.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <div className={`${course.color} p-6 text-white`}>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-1">{course.title}</h3>
                    <p className="text-white/80 text-sm">{course.code}</p>
                  </div>
                  <Badge variant="default" className="bg-white/20 text-white border-white/30">
                    {course.completedSessions}/{course.sessions}
                  </Badge>
                </div>
              </div>

              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <UsersIcon className="h-4 w-4 mr-1" />
                    <span>{course.instructor}</span>
                  </div>
                </div>

                {/* Engagement Indicator */}
                <div className="mb-4">
                  <EngagementIndicator
                    engagementLevel={course.engagementLevel}
                    engagementScore={course.engagement}
                    showCluster={false}
                  />
                </div>

                {/* Progress Bar */}
                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-medium text-gray-900">{course.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-indigo-600 h-2 rounded-full transition-all"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4 mb-4 pt-4 border-t border-gray-200">
                  <div>
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <UsersIcon className="h-4 w-4 mr-1" />
                      <span>Students</span>
                    </div>
                    <p className="text-lg font-semibold text-gray-900">{course.students}</p>
                  </div>
                  <div>
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <ClockIcon className="h-4 w-4 mr-1" />
                      <span>Sessions</span>
                      </div>
                    <p className="text-lg font-semibold text-gray-900">
                      {course.completedSessions}/{course.sessions}
                    </p>
                      </div>
                      </div>

                {/* Upcoming Session */}
                {course.upcomingSession && (
                  <div className="mb-4 p-3 bg-indigo-50 rounded-lg">
                    <div className="flex items-center text-sm text-indigo-900 mb-1">
                      <CalendarIcon className="h-4 w-4 mr-1" />
                      <span className="font-medium">Next Session</span>
                      </div>
                    <p className="text-sm text-indigo-700">{course.upcomingSession}</p>
                      </div>
                )}

                {/* Actions */}
                <div className="flex space-x-2">
                  <Link
                    to={`/dashboard/courses/${course.id}`}
                    className="flex-1 text-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 transition-colors"
                  >
                    View Details
                  </Link>
                  {course.upcomingSession && (
                    <Link
                      to={`/dashboard/sessions`}
                      className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50 transition-colors"
                    >
                      Join
                      </Link>
                  )}
                </div>
          </div>
            </Card>
          ))}
        </div>
      )}
      </div>
  );
};

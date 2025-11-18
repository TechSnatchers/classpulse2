import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
export const CourseCreate = () => {
  const {
    user
  } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    code: '',
    description: '',
    startDate: '',
    endDate: '',
    maxStudents: 30
  });
  const [isLoading, setIsLoading] = useState(false);
  const handleChange = e => {
    const {
      name,
      value
    } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  const handleSubmit = async e => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    // Redirect to courses page
    navigate(`/dashboard/${user?.role}/courses`);
    setIsLoading(false);
  };
  return <div>
      <h1 className="text-2xl font-semibold text-gray-900">
        Create New Course
      </h1>
      <p className="mt-1 text-sm text-gray-500">
        Fill in the details to create a new course.
      </p>
      <div className="mt-6 bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <div className="md:grid md:grid-cols-3 md:gap-6">
          <div className="md:col-span-1">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Course Information
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Basic information about the course you are creating.
            </p>
          </div>
          <div className="mt-5 md:mt-0 md:col-span-2">
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-6 gap-6">
                <div className="col-span-6 sm:col-span-4">
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Course Title
                  </label>
                  <input type="text" name="title" id="title" value={formData.title} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
                <div className="col-span-6 sm:col-span-2">
                  <label htmlFor="code" className="block text-sm font-medium text-gray-700">
                    Course Code
                  </label>
                  <input type="text" name="code" id="code" value={formData.code} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
                <div className="col-span-6">
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <textarea id="description" name="description" rows={3} value={formData.description} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
                <div className="col-span-6 sm:col-span-3">
                  <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">
                    Start Date
                  </label>
                  <input type="date" name="startDate" id="startDate" value={formData.startDate} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
                <div className="col-span-6 sm:col-span-3">
                  <label htmlFor="endDate" className="block text-sm font-medium text-gray-700">
                    End Date
                  </label>
                  <input type="date" name="endDate" id="endDate" value={formData.endDate} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
                <div className="col-span-6 sm:col-span-3">
                  <label htmlFor="maxStudents" className="block text-sm font-medium text-gray-700">
                    Maximum Students
                  </label>
                  <input type="number" name="maxStudents" id="maxStudents" min="1" value={formData.maxStudents} onChange={handleChange} className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" required />
                </div>
              </div>
              <div className="mt-6 flex justify-end">
                <button type="button" onClick={() => navigate(`/dashboard/${user?.role}/courses`)} className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  Cancel
                </button>
                <button type="submit" disabled={isLoading} className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  {isLoading ? 'Creating...' : 'Create Course'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>;
};
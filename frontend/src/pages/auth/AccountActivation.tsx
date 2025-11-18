import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
export const AccountActivation = () => {
  const {
    activateAccount
  } = useAuth();
  const navigate = useNavigate();
  const {
    token
  } = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    const activate = async () => {
      if (!token) {
        setError('Invalid activation link');
        setIsLoading(false);
        return;
      }
      try {
        const success = await activateAccount(token);
        setIsSuccess(success);
      } catch (err) {
        setError('Failed to activate account');
      } finally {
        setIsLoading(false);
      }
    };
    activate();
  }, [token, activateAccount]);
  return <div className="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Account Activation
        </h2>
      </div>
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {isLoading ? <div className="text-center">
              <div className="text-sm text-gray-700">
                Activating your account...
              </div>
            </div> : isSuccess ? <div className="text-center">
              <div className="text-sm text-gray-700 mb-4">
                Your account has been successfully activated!
              </div>
              <Link to="/login" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Login to your account
              </Link>
            </div> : <div className="text-center">
              <div className="text-sm text-red-600 mb-4">
                {error || 'Failed to activate account'}
              </div>
              <Link to="/login" className="text-indigo-600 hover:text-indigo-500">
                Return to login
              </Link>
            </div>}
        </div>
      </div>
    </div>;
};
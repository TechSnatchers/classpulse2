import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { SessionForm, SessionFormData } from '../../components/sessions/SessionForm';
import { Card } from '../../components/ui/Card';
import { ArrowLeftIcon } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { toast } from 'sonner';
import { sessionService } from '../../services/sessionService';

export const SessionEdit = () => {
  const navigate = useNavigate();
  const { sessionId } = useParams();
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [initialData, setInitialData] = useState<Partial<SessionFormData> | null>(null);
  const [loadingSession, setLoadingSession] = useState(true);

  // Check if user is instructor or admin
  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';

  useEffect(() => {
    // Load session data
    const loadSession = () => {
      try {
        if (sessionId) {
          const session = sessionService.getSessionById(sessionId);
          if (session) {
            setInitialData({
              title: session.title,
              course: session.course,
              courseCode: session.courseCode,
              date: session.date,
              startTime: session.startTime,
              endTime: session.endTime,
              duration: session.duration,
              description: session.description || '',
              materials: session.materials || []
            });
          } else {
            toast.error('Session not found.');
          }
        }
      } catch (error) {
        console.error('Error loading session:', error);
        toast.error('Failed to load session data.');
      } finally {
        setLoadingSession(false);
      }
    };

    if (sessionId) {
      loadSession();
    }
  }, [sessionId]);

  if (!isInstructor) {
    return (
      <div className="py-6">
        <Card className="p-6">
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Access Denied</h2>
            <p className="text-gray-600 mb-4">Only instructors can edit sessions.</p>
            <Button variant="primary" onClick={() => navigate('/dashboard/sessions')}>
              Go to Sessions
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  if (loadingSession) {
    return (
      <div className="py-6">
        <Card className="p-6">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading session...</p>
          </div>
        </Card>
      </div>
    );
  }

  if (!initialData) {
    return (
      <div className="py-6">
        <Card className="p-6">
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Session Not Found</h2>
            <p className="text-gray-600 mb-4">The session you're looking for doesn't exist.</p>
            <Button variant="primary" onClick={() => navigate('/dashboard/sessions')}>
              Go to Sessions
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  const handleSubmit = async (data: SessionFormData) => {
    setIsLoading(true);
    try {
      if (!sessionId) {
        toast.error('Session ID is missing.');
        return;
      }

      const updated = sessionService.updateSession(sessionId, {
        title: data.title,
        course: data.course,
        courseCode: data.courseCode,
        date: data.date,
        startTime: data.startTime,
        endTime: data.endTime,
        duration: data.duration,
        description: data.description,
        materials: data.materials || []
      });

      if (updated) {
        console.log('Session updated:', updated);
        toast.success('Session updated successfully!');
        navigate('/dashboard/sessions');
      } else {
        toast.error('Session not found.');
      }
    } catch (error) {
      console.error('Error updating session:', error);
      toast.error('Failed to update session. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="py-6">
      <div className="mb-6">
        <Button
          variant="outline"
          leftIcon={<ArrowLeftIcon className="h-4 w-4" />}
          onClick={() => navigate('/dashboard/sessions')}
          className="mb-4"
        >
          Back to Sessions
        </Button>
        <h1 className="text-2xl font-semibold text-gray-900">Edit Session</h1>
        <p className="mt-1 text-sm text-gray-500">
          Update the session details and materials
        </p>
      </div>

      <SessionForm
        initialData={initialData}
        onSubmit={handleSubmit}
        onCancel={() => navigate('/dashboard/sessions')}
        isLoading={isLoading}
      />
    </div>
  );
};


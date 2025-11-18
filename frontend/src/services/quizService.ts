// Quiz service for handling quiz-related API calls
import type { Question } from '../components/questions/QuestionBank';

export interface QuizAnswer {
  questionId: string;
  answerIndex: number;
  timeTaken: number;
  studentId: string;
  sessionId: string;
}

export interface QuizPerformance {
  totalStudents: number;
  answeredStudents: number;
  correctAnswers: number;
  averageTime: number;
  correctPercentage: number;
  performanceByCluster: {
    clusterName: string;
    answered: number;
    correct: number;
    percentage: number;
  }[];
  topPerformers: {
    studentName: string;
    isCorrect: boolean;
    timeTaken: number;
  }[];
}

export interface AssignedQuestionResponse {
  active: boolean;
  assignmentId?: string;
  question?: Question;
  completed?: boolean;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const getAuthToken = (): string => {
  try {
    const user = localStorage.getItem('user');
    if (user) {
      const userData = JSON.parse(user);
      return userData.token || 'mock-token';
    }
  } catch (error) {
    console.error('Error getting auth token:', error);
  }
  return 'mock-token';
};

const getUserRole = (): string => {
  try {
    const user = localStorage.getItem('user');
    if (user) {
      const userData = JSON.parse(user);
      return userData.role || 'student';
    }
  } catch (error) {
    console.error('Error getting user role:', error);
  }
  return 'student';
};

const getAuthHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${getAuthToken()}`,
  'x-user-role': getUserRole(),
});

export const quizService = {
  // Submit quiz answer
  async submitAnswer(answer: QuizAnswer): Promise<{ success: boolean; isCorrect: boolean }> {
    try {
      const response = await fetch(`${API_BASE_URL}/quiz/submit`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(answer),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', errorText);
        throw new Error(`Failed to submit answer: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting answer:', error);
      // Fallback for development if backend is not running
      console.warn('Using fallback mock data - backend may not be running');
      return {
        success: true,
        isCorrect: Math.random() > 0.3, // Mock: 70% correct
      };
    }
  },

  // Get default performance data
  getDefaultPerformance(): QuizPerformance {
    return {
      totalStudents: 32,
      answeredStudents: 28,
      correctAnswers: 20,
      averageTime: 12.5,
      correctPercentage: 71.4,
      performanceByCluster: [
        {
          clusterName: 'Active Participants',
          answered: 18,
          correct: 15,
          percentage: 83.3,
        },
        {
          clusterName: 'Moderate Participants',
          answered: 8,
          correct: 5,
          percentage: 62.5,
        },
        {
          clusterName: 'At-Risk Students',
          answered: 2,
          correct: 0,
          percentage: 0,
        },
      ],
      topPerformers: [
        { studentName: 'Alice Johnson', isCorrect: true, timeTaken: 8.2 },
        { studentName: 'Bob Williams', isCorrect: true, timeTaken: 9.5 },
        { studentName: 'Charlie Brown', isCorrect: false, timeTaken: 15.3 },
      ],
    };
  },

  // Get quiz performance
  async getQuizPerformance(questionId: string, sessionId: string): Promise<QuizPerformance> {
    if (!questionId || !sessionId) {
      console.warn('Missing questionId or sessionId for performance query');
      return this.getDefaultPerformance();
    }

    try {
      const encodedQuestionId = encodeURIComponent(questionId);
      const encodedSessionId = encodeURIComponent(sessionId);
      const response = await fetch(`${API_BASE_URL}/quiz/performance/${encodedQuestionId}?sessionId=${encodedSessionId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', response.status, errorText);
        throw new Error(`Failed to get quiz performance: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting quiz performance:', error);
      console.warn('Using fallback mock data - backend may not be running');
      // Return default performance data
      return this.getDefaultPerformance();
    }
  },

  // Trigger question (instructor only)
  async triggerQuestion(questionId: string, sessionId: string): Promise<{ success: boolean }> {
    try {
      const response = await fetch(`${API_BASE_URL}/quiz/trigger`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ questionId, sessionId }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', errorText);
        throw new Error(`Failed to trigger question: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error triggering question:', error);
      console.warn('Using fallback - backend may not be running');
      return { success: true };
    }
  },

  // Trigger personalized questions (unique per student)
  async triggerIndividualQuestions(sessionId: string): Promise<{ success: boolean; mode?: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/quiz/trigger/individual`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ sessionId }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', errorText);
        throw new Error(`Failed to trigger personalized questions: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error triggering personalized questions:', error);
      throw error;
    }
  },

  // Get personalized assignment for a student
  async getAssignedQuestion(sessionId: string, studentId: string): Promise<AssignedQuestionResponse> {
    if (!sessionId || !studentId) {
      return { active: false };
    }

    try {
      const encodedSessionId = encodeURIComponent(sessionId);
      const encodedStudentId = encodeURIComponent(studentId);
      const response = await fetch(`${API_BASE_URL}/quiz/assignment?sessionId=${encodedSessionId}&studentId=${encodedStudentId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 404) {
          return { active: false };
        }
        const errorText = await response.text();
        console.error('API Error:', errorText);
        throw new Error(`Failed to get assignment: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting personalized assignment:', error);
      return { active: false };
    }
  },
};


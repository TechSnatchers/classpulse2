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


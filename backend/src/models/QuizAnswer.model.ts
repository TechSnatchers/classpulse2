export interface QuizAnswer {
  questionId: string;
  answerIndex: number;
  timeTaken: number; // in seconds
  studentId: string;
  sessionId: string;
  timestamp: Date;
}

export class QuizAnswerModel {
  questionId: string;
  answerIndex: number;
  timeTaken: number;
  studentId: string;
  sessionId: string;
  timestamp: Date;

  constructor(data: Partial<QuizAnswer>) {
    this.questionId = data.questionId || '';
    this.answerIndex = data.answerIndex ?? -1;
    this.timeTaken = data.timeTaken || 0;
    this.studentId = data.studentId || '';
    this.sessionId = data.sessionId || '';
    this.timestamp = data.timestamp || new Date();
  }
}


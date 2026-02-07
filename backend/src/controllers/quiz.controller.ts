import { Request, Response } from 'express';
import { QuizService } from '../services/quiz.service';

export class QuizController {
  private quizService: QuizService;

  constructor() {
    this.quizService = new QuizService();
  }

  async submitAnswer(req: Request, res: Response) {
    try {
      const { questionId, answerIndex, timeTaken, studentId, sessionId } = req.body;

      if (!questionId || answerIndex === undefined || !timeTaken || !studentId || !sessionId) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      const result = await this.quizService.submitAnswer({
        questionId,
        answerIndex,
        timeTaken,
        studentId,
        sessionId,
      });

      res.json(result);
    } catch (error) {
      console.error('Error submitting answer:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getPerformance(req: Request, res: Response) {
    try {
      const { questionId } = req.params;
      const { sessionId } = req.query;

      if (!questionId || !sessionId) {
        return res.status(400).json({ error: 'Missing required parameters', questionId, sessionId });
      }

      // Check if user is instructor (for development, allow all)
      const user = (req as any).user;
      if (user && user.role !== 'instructor' && user.role !== 'admin') {
        // For development, we'll still allow but log a warning
        console.warn('Non-instructor accessing performance data');
      }

      const performance = await this.quizService.getPerformance(questionId, sessionId as string);

      res.json(performance);
    } catch (error: any) {
      console.error('Error getting performance:', error);
      res.status(500).json({ 
        error: 'Internal server error',
        message: error.message 
      });
    }
  }

  async triggerQuestion(req: Request, res: Response) {
    try {
      const { questionId, sessionId } = req.body;

      if (!questionId || !sessionId) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      // Check if user is instructor
      const user = (req as any).user;
      if (user.role !== 'instructor' && user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden: Instructor access required' });
      }

      await this.quizService.triggerQuestion(questionId, sessionId);

      res.json({ success: true });
    } catch (error) {
      console.error('Error triggering question:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}


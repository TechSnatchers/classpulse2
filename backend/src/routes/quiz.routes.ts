import { Router } from 'express';
import { QuizController } from '../controllers/quiz.controller';
import { authMiddleware } from '../middleware/auth.middleware';

const router = Router();
const quizController = new QuizController();

// Submit quiz answer
router.post('/submit', authMiddleware, quizController.submitAnswer.bind(quizController));

// Get quiz performance (instructor only)
router.get('/performance/:questionId', authMiddleware, quizController.getPerformance.bind(quizController));

// Trigger question (instructor only)
router.post('/trigger', authMiddleware, quizController.triggerQuestion.bind(quizController));

export default router;


import { Router } from 'express';
import { ClusteringController } from '../controllers/clustering.controller';
import { authMiddleware } from '../middleware/auth.middleware';

const router = Router();
const clusteringController = new ClusteringController();

// Get clusters for a session
router.get('/session/:sessionId', authMiddleware, clusteringController.getClusters.bind(clusteringController));

// Update clusters based on quiz performance
router.post('/update', authMiddleware, clusteringController.updateClusters.bind(clusteringController));

// Get student's cluster assignment
router.get('/student/:studentId', authMiddleware, clusteringController.getStudentCluster.bind(clusteringController));

export default router;


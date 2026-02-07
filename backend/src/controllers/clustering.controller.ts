import { Request, Response } from 'express';
import { ClusteringService } from '../services/clustering.service';

export class ClusteringController {
  private clusteringService: ClusteringService;

  constructor() {
    this.clusteringService = new ClusteringService();
  }

  async getClusters(req: Request, res: Response) {
    try {
      const { sessionId } = req.params;

      if (!sessionId) {
        return res.status(400).json({ error: 'Missing sessionId', received: req.params });
      }

      console.log(`Getting clusters for session: ${sessionId}`);
      const clusters = await this.clusteringService.getClusters(sessionId);
      console.log(`Returning ${clusters.length} clusters for session ${sessionId}`);

      res.json(clusters);
    } catch (error: any) {
      console.error('Error getting clusters:', error);
      res.status(500).json({ 
        error: 'Internal server error',
        message: error.message 
      });
    }
  }

  async updateClusters(req: Request, res: Response) {
    try {
      const { sessionId, quizPerformance } = req.body;

      if (!sessionId) {
        return res.status(400).json({ error: 'Missing sessionId', received: req.body });
      }

      console.log(`Updating clusters for session: ${sessionId}`, quizPerformance);
      const clusters = await this.clusteringService.updateClusters({
        sessionId,
        quizPerformance,
      });

      res.json(clusters);
    } catch (error: any) {
      console.error('Error updating clusters:', error);
      res.status(500).json({ 
        error: 'Internal server error',
        message: error.message 
      });
    }
  }

  async getStudentCluster(req: Request, res: Response) {
    try {
      const { studentId } = req.params;
      const { sessionId } = req.query;

      if (!studentId || !sessionId) {
        return res.status(400).json({ error: 'Missing required parameters' });
      }

      const clusterId = await this.clusteringService.getStudentCluster(
        studentId,
        sessionId as string
      );

      res.json({ clusterId });
    } catch (error) {
      console.error('Error getting student cluster:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}


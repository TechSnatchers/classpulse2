import { StudentCluster } from '../models/Cluster.model';
import { Student } from '../models/Student.model';
import { QuizAnswer } from '../models/QuizAnswer.model';

interface ClusterUpdate {
  sessionId: string;
  quizPerformance?: {
    questionId: string;
    correctPercentage: number;
  };
}

export class ClusteringService {
  private clusters: Map<string, StudentCluster[]> = new Map(); // sessionId -> clusters
  private static instance: ClusteringService;

  constructor() {
    if (ClusteringService.instance) {
      return ClusteringService.instance;
    }
    ClusteringService.instance = this;
  }

  async getClusters(sessionId: string): Promise<StudentCluster[]> {
    if (this.clusters.has(sessionId)) {
      return this.clusters.get(sessionId)!;
    }

    // Initialize default clusters
    const defaultClusters: StudentCluster[] = [
      {
        id: '1',
        name: 'Active Participants',
        description: 'Highly engaged students',
        studentCount: 18,
        engagementLevel: 'high',
        color: '#10b981',
        prediction: 'stable',
        students: [],
      },
      {
        id: '2',
        name: 'Moderate Participants',
        description: 'Moderately engaged students',
        studentCount: 10,
        engagementLevel: 'medium',
        color: '#f59e0b',
        prediction: 'improving',
        students: [],
      },
      {
        id: '3',
        name: 'At-Risk Students',
        description: 'Low engagement, need support',
        studentCount: 4,
        engagementLevel: 'low',
        color: '#ef4444',
        prediction: 'declining',
        students: [],
      },
    ];

    this.clusters.set(sessionId, defaultClusters);
    return defaultClusters;
  }

  async updateClusters(update: ClusterUpdate): Promise<StudentCluster[]> {
    let clusters = await this.getClusters(update.sessionId);

    if (update.quizPerformance) {
      // Update clusters based on quiz performance
      clusters = this.recalculateClusters(clusters, update.quizPerformance);
      this.clusters.set(update.sessionId, clusters);
    }

    return clusters;
  }

  private recalculateClusters(
    currentClusters: StudentCluster[],
    quizPerformance: { questionId: string; correctPercentage: number }
  ): StudentCluster[] {
    // Simple clustering algorithm based on quiz performance
    // In a real implementation, this would consider:
    // - Quiz performance
    // - Response time
    // - Engagement metrics
    // - Historical data

    const performance = quizPerformance.correctPercentage;

    // Adjust cluster sizes based on performance
    // High performance (>80%) -> more students in active cluster
    // Low performance (<60%) -> more students in at-risk cluster

    const totalStudents = currentClusters.reduce((sum, c) => sum + c.studentCount, 0);

    if (performance >= 80) {
      // High performance: shift students to active cluster
      return [
        {
          ...currentClusters[0],
          studentCount: Math.min(totalStudents, Math.floor(totalStudents * 0.6)),
          prediction: 'stable' as const,
        },
        {
          ...currentClusters[1],
          studentCount: Math.floor(totalStudents * 0.3),
          prediction: 'improving' as const,
        },
        {
          ...currentClusters[2],
          studentCount: Math.max(0, totalStudents - Math.floor(totalStudents * 0.6) - Math.floor(totalStudents * 0.3)),
          prediction: 'declining' as const,
        },
      ];
    } else if (performance < 60) {
      // Low performance: shift students to at-risk cluster
      return [
        {
          ...currentClusters[0],
          studentCount: Math.floor(totalStudents * 0.4),
          prediction: 'stable' as const,
        },
        {
          ...currentClusters[1],
          studentCount: Math.floor(totalStudents * 0.3),
          prediction: 'declining' as const,
        },
        {
          ...currentClusters[2],
          studentCount: totalStudents - Math.floor(totalStudents * 0.4) - Math.floor(totalStudents * 0.3),
          prediction: 'declining' as const,
        },
      ];
    }

    // Medium performance: keep current distribution
    return currentClusters;
  }

  async getStudentCluster(studentId: string, sessionId: string): Promise<string | null> {
    const clusters = await this.getClusters(sessionId);
    
    // Find which cluster contains this student
    for (const cluster of clusters) {
      if (cluster.students.includes(studentId)) {
        return cluster.id;
      }
    }

    return null;
  }
}


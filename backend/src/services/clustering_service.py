from typing import Dict, List, Optional
from ..models.cluster import StudentCluster
from ..models.cluster_model import ClusterModel


class ClusteringService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClusteringService, cls).__new__(cls)
        return cls._instance

    async def get_clusters(self, session_id: str) -> List[StudentCluster]:
        """Get clusters from MongoDB or create default ones"""
        # Try to get clusters from database
        cluster_docs = await ClusterModel.find_by_session(session_id)
        
        if len(cluster_docs) > 0:
            # Convert to StudentCluster objects
            return [StudentCluster(**doc) for doc in cluster_docs]

        # Initialize default clusters if none exist
        default_clusters = [
            StudentCluster(
                id="1",
                name="Active Participants",
                description="Highly engaged students",
                studentCount=18,
                engagementLevel="high",
                color="#10b981",
                prediction="stable",
                students=[],
            ),
            StudentCluster(
                id="2",
                name="Moderate Participants",
                description="Moderately engaged students",
                studentCount=10,
                engagementLevel="medium",
                color="#f59e0b",
                prediction="improving",
                students=[],
            ),
            StudentCluster(
                id="3",
                name="At-Risk Students",
                description="Low engagement, need support",
                studentCount=4,
                engagementLevel="low",
                color="#ef4444",
                prediction="declining",
                students=[],
            ),
        ]

        # Save default clusters to database
        await ClusterModel.update_clusters_for_session(session_id, default_clusters)
        return default_clusters

    async def update_clusters(
        self,
        session_id: str,
        quiz_performance: Optional[Dict] = None
    ) -> List[StudentCluster]:
        """Update clusters in MongoDB"""
        clusters = await self.get_clusters(session_id)

        if quiz_performance:
            # Update clusters based on quiz performance
            clusters = self._recalculate_clusters(clusters, quiz_performance)
            # Save to database
            await ClusterModel.update_clusters_for_session(session_id, clusters)

        return clusters

    def _recalculate_clusters(
        self,
        current_clusters: List[StudentCluster],
        quiz_performance: Dict
    ) -> List[StudentCluster]:
        # Simple clustering algorithm based on quiz performance
        # In a real implementation, this would consider:
        # - Quiz performance
        # - Response time
        # - Engagement metrics
        # - Historical data

        performance = quiz_performance.get("correctPercentage", 0)

        # Adjust cluster sizes based on performance
        # High performance (>80%) -> more students in active cluster
        # Low performance (<60%) -> more students in at-risk cluster

        total_students = sum(c.studentCount for c in current_clusters)

        if performance >= 80:
            # High performance: shift students to active cluster
            return [
                StudentCluster(
                    **current_clusters[0].model_dump(),
                    studentCount=min(total_students, int(total_students * 0.6)),
                    prediction="stable",
                ),
                StudentCluster(
                    **current_clusters[1].model_dump(),
                    studentCount=int(total_students * 0.3),
                    prediction="improving",
                ),
                StudentCluster(
                    **current_clusters[2].model_dump(),
                    studentCount=max(
                        0,
                        total_students
                        - int(total_students * 0.6)
                        - int(total_students * 0.3)
                    ),
                    prediction="declining",
                ),
            ]
        elif performance < 60:
            # Low performance: shift students to at-risk cluster
            return [
                StudentCluster(
                    **current_clusters[0].model_dump(),
                    studentCount=int(total_students * 0.4),
                    prediction="stable",
                ),
                StudentCluster(
                    **current_clusters[1].model_dump(),
                    studentCount=int(total_students * 0.3),
                    prediction="declining",
                ),
                StudentCluster(
                    **current_clusters[2].model_dump(),
                    studentCount=total_students
                    - int(total_students * 0.4)
                    - int(total_students * 0.3),
                    prediction="declining",
                ),
            ]

        # Medium performance: keep current distribution
        return current_clusters

    async def get_student_cluster(
        self, student_id: str, session_id: str
    ) -> Optional[str]:
        """Get student's cluster from MongoDB"""
        cluster_id = await ClusterModel.find_student_cluster(student_id, session_id)
        return cluster_id


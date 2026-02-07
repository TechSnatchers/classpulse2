from typing import List, Optional
from bson import ObjectId
from ..database.connection import get_database
from .cluster import StudentCluster


class ClusterModel:
    @staticmethod
    async def find_by_session(session_id: str) -> List[dict]:
        """Find clusters for a session"""
        database = get_database()
        if database is None:
            return []
        
        clusters = []
        async for cluster in database.clusters.find({"sessionId": session_id}):
            cluster["id"] = str(cluster["_id"])
            del cluster["_id"]
            clusters.append(cluster)
        return clusters

    @staticmethod
    async def create(cluster_data: dict) -> dict:
        """Create a cluster"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")
        
        result = await database.clusters.insert_one(cluster_data)
        cluster_data["id"] = str(result.inserted_id)
        return cluster_data

    @staticmethod
    async def update_clusters_for_session(session_id: str, clusters: List[StudentCluster]) -> List[dict]:
        """Update clusters for a session (replace all)"""
        database = get_database()
        if database is None:
            return []
        
        # Delete existing clusters for this session
        await database.clusters.delete_many({"sessionId": session_id})
        
        # Insert new clusters
        cluster_docs = []
        for cluster in clusters:
            cluster_data = cluster.model_dump()
            cluster_data["sessionId"] = session_id
            result = await database.clusters.insert_one(cluster_data)
            cluster_data["id"] = str(result.inserted_id)
            cluster_docs.append(cluster_data)
        
        return cluster_docs

    @staticmethod
    async def find_student_cluster(student_id: str, session_id: str) -> Optional[str]:
        """Find which cluster a student belongs to"""
        database = get_database()
        if database is None:
            return None
        
        async for cluster in database.clusters.find({"sessionId": session_id}):
            if student_id in cluster.get("students", []):
                return str(cluster["_id"])
        return None


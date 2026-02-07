from typing import List
from pydantic import BaseModel


class PerformanceByCluster(BaseModel):
    clusterName: str
    answered: int
    correct: int
    percentage: float


class TopPerformer(BaseModel):
    studentName: str
    isCorrect: bool
    timeTaken: float


class QuizPerformance(BaseModel):
    totalStudents: int
    answeredStudents: int
    correctAnswers: int
    averageTime: float
    correctPercentage: float
    performanceByCluster: List[PerformanceByCluster]
    topPerformers: List[TopPerformer]


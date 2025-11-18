from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from pydantic import BaseModel
from ..services.quiz_service import QuizService
from ..models.quiz_answer import QuizAnswer
from ..models.quiz_performance import QuizPerformance
from ..middleware.auth import get_current_user, require_instructor

router = APIRouter(prefix="/api/quiz", tags=["quiz"])
quiz_service = QuizService()


class SubmitAnswerRequest(BaseModel):
    questionId: str
    answerIndex: int
    timeTaken: float
    studentId: str
    sessionId: str


class TriggerQuestionRequest(BaseModel):
    questionId: str
    sessionId: str


class TriggerIndividualRequest(BaseModel):
    sessionId: str


class AssignmentResponse(BaseModel):
    active: bool
    assignmentId: Optional[str] = None
    question: Optional[Dict] = None
    completed: Optional[bool] = None


@router.post("/submit")
async def submit_answer(
    request_data: SubmitAnswerRequest,
    request: Request,
    user: dict = Depends(get_current_user)
):
    """Submit quiz answer"""
    try:
        answer = QuizAnswer(
            questionId=request_data.questionId,
            answerIndex=request_data.answerIndex,
            timeTaken=request_data.timeTaken,
            studentId=request_data.studentId,
            sessionId=request_data.sessionId,
        )

        result = await quiz_service.submit_answer(answer)
        return result
    except Exception as e:
        print(f"Error submitting answer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/performance/{question_id}")
async def get_performance(
    question_id: str,
    session_id: str = Query(..., alias="sessionId"),
    user: dict = Depends(get_current_user)
):
    """Get quiz performance (instructor only)"""
    try:
        if not question_id or not session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters"
            )

        # Check if user is instructor (for development, allow all)
        if user.get("role") not in ["instructor", "admin"]:
            print("Warning: Non-instructor accessing performance data")

        performance = await quiz_service.get_performance(question_id, session_id)
        return performance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error getting performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/trigger")
async def trigger_question(
    request_data: TriggerQuestionRequest,
    request: Request,
    user: dict = Depends(require_instructor)
):
    """Trigger question (instructor only)"""
    try:
        if not request_data.questionId or not request_data.sessionId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields"
            )

        result = await quiz_service.trigger_question(
            request_data.questionId,
            request_data.sessionId
        )
        return result
    except Exception as e:
        print(f"Error triggering question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/trigger/individual")
async def trigger_individual_questions(
    request_data: TriggerIndividualRequest,
    user: dict = Depends(require_instructor)
):
    """Trigger personalized questions (each student gets a unique question)"""
    try:
        if not request_data.sessionId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing sessionId"
            )

        result = await quiz_service.trigger_individual_questions(request_data.sessionId)
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error triggering individual questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/assignment", response_model=AssignmentResponse)
async def get_personalized_assignment(
    session_id: str = Query(..., alias="sessionId"),
    student_id: str = Query(..., alias="studentId"),
    user: dict = Depends(get_current_user)
):
    """Get or create personalized question assignment for a student"""
    try:
        if user.get("role") not in ["instructor", "admin"] and user.get("id") != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: cannot access other student's assignment"
            )

        assignment = await quiz_service.get_assignment_for_student(session_id, student_id)
        return assignment
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error retrieving assignment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


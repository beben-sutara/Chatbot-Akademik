from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.chat import ChatSession, ChatMessage, MessageRole
from ..schemas.chat import ChatRequest, ChatResponse, ChatSessionOut
from ..utils.auth import get_current_user
from ..services.ai_service import get_ai_response

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get or create session
    if request.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == request.session_id,
            ChatSession.user_id == current_user.id,
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Sesi chat tidak ditemukan")
    else:
        title = request.message[:50] + ("..." if len(request.message) > 50 else "")
        session = ChatSession(user_id=current_user.id, title=title)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(session_id=session.id, role=MessageRole.user, content=request.message)
    db.add(user_msg)
    db.commit()

    # Get conversation history
    history = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at).all()

    # Get AI response
    ai_reply = await get_ai_response(
        message=request.message,
        history=history,
        user=current_user,
        db=db,
    )

    # Save assistant message
    ai_msg = ChatMessage(session_id=session.id, role=MessageRole.assistant, content=ai_reply)
    db.add(ai_msg)
    db.commit()

    return ChatResponse(session_id=session.id, message=ai_reply)


@router.get("/sessions", response_model=List[ChatSessionOut])
def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.created_at.desc()).all()


@router.get("/sessions/{session_id}", response_model=ChatSessionOut)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesi chat tidak ditemukan")
    return session


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesi chat tidak ditemukan")
    db.delete(session)
    db.commit()
    return {"message": "Sesi chat dihapus"}

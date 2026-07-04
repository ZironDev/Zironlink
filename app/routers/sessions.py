# Zironlink -- public redacted build. Full source in the private repo.

from fastapi import APIRouter, HTTPException
from app.models import SessionUpdateRequest
from app.ws_manager import ws_manager
router = APIRouter()

@router.patch('/v4/sessions/{session_id}')
async def update_session(session_id: str, body: SessionUpdateRequest):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

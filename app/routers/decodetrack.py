# Zironlink -- public redacted build. Full source in the private repo.

from typing import List
from fastapi import APIRouter, Query, Body, HTTPException
from app.track_codec import decode_track
from app.models import Track
router = APIRouter()

@router.get('/v4/decodetrack')
async def decodetrack(encodedTrack: str=Query(...)):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.post('/v4/decodetracks')
async def decodetracks(encoded: List[str]=Body(...)):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

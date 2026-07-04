# Zironlink -- public redacted build. Full source in the private repo.

from fastapi import APIRouter, Query
from app.track_loader import load_item
router = APIRouter()

@router.get('/v4/loadtracks')
async def loadtracks(identifier: str=Query(...)):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

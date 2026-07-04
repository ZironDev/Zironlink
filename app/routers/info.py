# Zironlink -- public redacted build. Full source in the private repo.

import time
from fastapi import APIRouter
from app.config import settings
from app.state import players
from app.ws_manager import ws_manager
router = APIRouter()
_START_TIME = time.time()

@router.get('/version')
async def version():
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/info')
async def info():
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/stats')
async def stats():
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

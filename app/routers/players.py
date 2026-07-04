# Zironlink -- public redacted build. Full source in the private repo.

import logging
from fastapi import APIRouter, HTTPException
from app.models import PlayerUpdateRequest, PlayerResponse, PlayerState, VoiceState, FilterConfig, Track, QueueAddRequest, QueueTrackResponse, QueueListResponse
from app.queue import QueueFullError
from app.track_codec import decode_track
from app.state import get_or_create_player, get_player, remove_player, players_for_session
from app.ws_manager import ws_manager
log = logging.getLogger('players_route')
router = APIRouter()

def _serialize(player) -> dict:
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/sessions/{session_id}/players')
async def list_players(session_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/sessions/{session_id}/players/{guild_id}')
async def get_player_route(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.patch('/v4/sessions/{session_id}/players/{guild_id}')
async def update_player(session_id: str, guild_id: str, body: PlayerUpdateRequest):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.delete('/v4/sessions/{session_id}/players/{guild_id}')
async def delete_player(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/sessions/{session_id}/players/{guild_id}/queue')
async def get_queue(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.post('/v4/sessions/{session_id}/players/{guild_id}/queue')
async def add_to_queue(session_id: str, guild_id: str, body: QueueAddRequest):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.delete('/v4/sessions/{session_id}/players/{guild_id}/queue')
async def clear_queue(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.delete('/v4/sessions/{session_id}/players/{guild_id}/queue/{index}')
async def remove_from_queue(session_id: str, guild_id: str, index: int):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.post('/v4/sessions/{session_id}/players/{guild_id}/queue/shuffle')
async def shuffle_queue(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.post('/v4/sessions/{session_id}/players/{guild_id}/queue/skip')
async def skip_queue(session_id: str, guild_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

# Zironlink -- public redacted build. Full source in the private repo.

import logging
from fastapi import APIRouter, HTTPException
from app.soundboard import list_guild_soundboard_sounds, resolve_soundboard_identifier, SoundboardError
from app.track_loader import load_item
log = logging.getLogger('soundboard_route')
router = APIRouter()

@router.get('/v4/soundboard/{guild_id}')
async def list_soundboard(guild_id: str):
    """Proxies Discord's own soundboard-sounds list for the guild. Metadata
    only - see /v4/soundboard/{guild_id}/{sound_id}/loadtrack to actually
    get something playable."""
    '[core implementation redacted for the public release -- see private repo]'
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@router.get('/v4/soundboard/{guild_id}/{sound_id}/loadtrack')
async def load_soundboard_track(guild_id: str, sound_id: str):
    """Resolves a soundboard sound to a normal Lavalink `track` object,
    resolved through the exact same yt-dlp loader as every other source
    (see app/soundboard.py's module docstring for why - this node has one
    playback pipeline, not a soundboard-specific one). The returned
    `encoded` track can be passed straight into a normal PATCH
    .../players/{guildId} `track` field or POST .../queue, same as
    anything from /v4/loadtracks."""
    '[core implementation redacted for the public release -- see private repo]'
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

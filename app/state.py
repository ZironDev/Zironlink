# Zironlink -- public redacted build. Full source in the private repo.

from typing import Dict, Tuple
from app.player import Player
players: Dict[Tuple[str, str], Player] = {}

def get_player(session_id: str, guild_id: str) -> Player | None:
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

def get_or_create_player(session_id: str, guild_id: str, user_id: str) -> Player:
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

async def remove_player(session_id: str, guild_id: str) -> None:
    """[core implementation redacted for the public release -- see private repo]"""

def players_for_session(session_id: str):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

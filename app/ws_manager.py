# Zironlink -- public redacted build. Full source in the private repo.

import asyncio
import json
import logging
import time
from typing import Dict, Optional
from fastapi import WebSocket
log = logging.getLogger('ws_manager')

class ClientSession:

    def __init__(self, session_id: str, websocket: WebSocket, user_id: str):
        """[core implementation redacted for the public release -- see private repo]"""

    async def send(self, payload: dict) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

class WSManager:

    def __init__(self):
        """[core implementation redacted for the public release -- see private repo]"""

    def register(self, session: ClientSession) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def unregister(self, session_id: str) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def get(self, session_id: str) -> Optional[ClientSession]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    async def emit(self, session_id: str, payload: dict) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def emit_player_event(self, session_id: str, guild_id: str, event_type: str, **extra) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def emit_player_update(self, session_id: str, guild_id: str, position: int, connected: bool, ping: int=-1) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def build_stats_payload(self, player_count: int, playing_count: int) -> dict:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')
ws_manager = WSManager()

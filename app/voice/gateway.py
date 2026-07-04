# Zironlink -- public redacted build. Full source in the private repo.

import asyncio
import json
import logging
from typing import Optional, Callable, Awaitable
import websockets
from app.voice.udp import VoiceUDPClient, ENCRYPTION_MODE
from app.voice.dave_session import DaveSession, max_supported_protocol_version
log = logging.getLogger('voice.gateway')
VOICE_CLOSE_CODES = {4001: 'unknown opcode', 4002: 'failed to decode payload', 4003: 'not authenticated (identify not sent before something else)', 4004: 'authentication failed (bad token)', 4005: 'already authenticated', 4006: 'session no longer valid', 4009: 'session timed out', 4011: 'server not found', 4012: 'unknown protocol', 4014: 'disconnected (channel deleted / kicked / voice server changed)', 4015: 'voice server crashed', 4016: 'unknown encryption mode'}
CONNECT_TIMEOUT_SECONDS = 10
OP_IDENTIFY = 0
OP_SELECT_PROTOCOL = 1
OP_READY = 2
OP_HEARTBEAT = 3
OP_SESSION_DESCRIPTION = 4
OP_SPEAKING = 5
OP_HEARTBEAT_ACK = 6
OP_HELLO = 8
OP_RESUMED = 9
OP_CLIENT_DISCONNECT = 13
OP_DAVE_PREPARE_TRANSITION = 21
OP_DAVE_EXECUTE_TRANSITION = 22
OP_DAVE_TRANSITION_READY = 23
OP_DAVE_PREPARE_EPOCH = 24
OP_DAVE_MLS_EXTERNAL_SENDER = 25
OP_DAVE_MLS_KEY_PACKAGE = 26
OP_DAVE_MLS_PROPOSALS = 27
OP_DAVE_MLS_COMMIT_WELCOME = 28
OP_DAVE_MLS_ANNOUNCE_COMMIT_TRANSITION = 29
OP_DAVE_MLS_WELCOME = 30
OP_DAVE_MLS_INVALID_COMMIT_WELCOME = 31

class VoiceGateway:

    def __init__(self, guild_id: str, user_id: str, session_id: str, token: str, endpoint: str, channel_id: Optional[str]=None, on_ready: Optional[Callable[[], Awaitable[None]]]=None):
        """[core implementation redacted for the public release -- see private repo]"""

    async def connect(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _send_json(self, payload: dict) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _send_binary(self, opcode: int, payload: bytes=b'') -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _recv_loop(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _handle_binary(self, data: bytes) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _send_transition_ready(self, transition_id: int) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _handle(self, data: dict) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def _heartbeat_loop(self, interval: float) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def set_speaking(self, speaking: bool) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    async def close(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

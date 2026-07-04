# Zironlink -- public redacted build. Full source in the private repo.

import logging
from typing import Optional
import dave
log = logging.getLogger('voice.dave')
MEDIA_TYPE_AUDIO = dave.MediaType.audio

def max_supported_protocol_version() -> int:
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

class DaveSession:

    def __init__(self, guild_id: str, own_user_id: str, channel_id: Optional[str]=None):
        """[core implementation redacted for the public release -- see private repo]"""

    def _get_transient_key(self, version: int) -> 'dave.SignatureKeyPair':
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def start(self, protocol_version: int) -> None:
        """Called on receiving OP4 Session Description's dave_protocol_version."""
        '[core implementation redacted for the public release -- see private repo]'

    def _on_mls_failure(self, reason: str, detail: str) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def note_speaker(self, user_id: str) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def set_external_sender(self, payload: bytes) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def make_key_package(self) -> bytes:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def apply_proposals(self, payload: bytes) -> Optional[bytes]:
        """Append/revoke proposals and produce our commit (+ bundled welcome
        if applicable). Returned bytes, if any, should be sent verbatim as
        the OP28 (DAVE MLS Commit Welcome) payload.

        UNVERIFIED: process_proposals()'s return value is assumed to already
        be the wire-ready "commit welcome" blob (there's no separate
        create_commit()/get_welcome() call exposed in the stub), matching
        the fact that opcode 28 is itself named "Commit Welcome" (a single
        bundled message).
        """
        '[core implementation redacted for the public release -- see private repo]'
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def apply_commit(self, payload: bytes):
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def apply_welcome(self, payload: bytes):
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def refresh_own_key_ratchet(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def refresh_decryptor(self, speaker_user_id: str) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

    def encrypt(self, ssrc: int, opus_frame: bytes) -> bytes:
        """Encrypt one outgoing Opus frame. Falls back to plaintext (transport
        encryption still applies downstream) if DAVE isn't active or the
        encryptor has no key ratchet yet, e.g. mid-transition."""
        '[core implementation redacted for the public release -- see private repo]'
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def decrypt(self, speaker_user_id: str, frame: bytes) -> Optional[bytes]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def downgrade(self) -> None:
        """Called on a transition to protocol version 0 (e.g. a non-DAVE
        client joined). Stop E2EE, fall back to transport-only encryption."""
        '[core implementation redacted for the public release -- see private repo]'

    def reset(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

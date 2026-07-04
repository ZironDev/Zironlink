# Zironlink -- public redacted build. Full source in the private repo.

from __future__ import annotations
import random
from collections import deque
from typing import Deque, List, Optional
from app.models import Track

class QueueFullError(Exception):
    pass

class TrackQueue:

    def __init__(self, guild_id: str, max_size: int):
        """[core implementation redacted for the public release -- see private repo]"""

    def __len__(self) -> int:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    @property
    def is_full(self) -> bool:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def list(self) -> List[Track]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def add(self, track: Track) -> int:
        """Appends a track. Returns its 1-based position in the queue.
        Raises QueueFullError if the guild's queue is already at max_size."""
        '[core implementation redacted for the public release -- see private repo]'
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def pop_next(self) -> Optional[Track]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def peek_next(self) -> Optional[Track]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def remove_at(self, index: int) -> Optional[Track]:
        """0-based index, matching the order returned by list()."""
        '[core implementation redacted for the public release -- see private repo]'
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def clear(self) -> List[Track]:
        """[core implementation redacted for the public release -- see private repo]"""
        raise NotImplementedError('core implementation redacted for the public release -- see private repo')

    def shuffle(self) -> None:
        """[core implementation redacted for the public release -- see private repo]"""

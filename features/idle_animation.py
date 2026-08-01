# ─────────────────────────────────────────────
# features/idle_animation.py – Outer ring SMR
#     grid animation when controller is idle
# ─────────────────────────────────────────────

import time
import midi
import mixer
import transport
from device import midiOutMsg

from config import (
    MIDI_CHANNEL,
    SMR_GRID_CC,
    IDLE_TIMEOUT_SEC,
    IDLE_TICKS_PER_STEP,
    IDLE_TRAIL_LENGTH
)

# ── Outer ring sequence ──────────────────────
# Traverses top row (left->right), right edge,
# bottom row (right->left), left edge.
_OUTER_RING = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 7),
    (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0),
    (1, 0)
]
_RING_LEN = len(_OUTER_RING)

# ── State ────────────────────────────────────
_last_activity = time.time()
_active = False
_tick = 0
_head_pos = 0


def _set_led(row, col, on):
    """Turn a single SMR grid LED on or off."""
    cc = SMR_GRID_CC[row][col]
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, 127 if on else 0)


def _stop():
    """Stop animation and clear LEDs."""
    global _active, _tick, _head_pos
    _active = False
    _tick = 0
    _head_pos = 0
    for r, c in _OUTER_RING:
        _set_led(r, c, False)


def notify_activity():
    """Reset the idle timer. Call this on any controller action."""
    global _last_activity, _active
    _last_activity = time.time()
    if _active:
        _stop()


def tick():
    """Advance the animation if idle."""
    global _active, _last_activity, _tick, _head_pos

    # If the track is playing or audio is passing through the master mixer, we are not idle.
    if transport.isPlaying() or mixer.getLastPeakVol(0) > 0.005 or mixer.getLastPeakVol(1) > 0.005:
        notify_activity()
        return False

    if not _active:
        if time.time() - _last_activity >= IDLE_TIMEOUT_SEC:
            # Become active
            _active = True
            _tick = 0
            _head_pos = 0
        else:
            return False

    if _tick % IDLE_TICKS_PER_STEP == 0:
        # Turn off the trailing LED
        tail_pos = (_head_pos - IDLE_TRAIL_LENGTH) % _RING_LEN
        tr, tc = _OUTER_RING[tail_pos]
        _set_led(tr, tc, False)

        # Turn on the new head LED
        hr, hc = _OUTER_RING[_head_pos]
        _set_led(hr, hc, True)

        _head_pos = (_head_pos + 1) % _RING_LEN

    _tick += 1
    return True

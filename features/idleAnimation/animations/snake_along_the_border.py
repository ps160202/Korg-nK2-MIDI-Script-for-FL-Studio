import midi
from device import midiOutMsg

from config import (
    MIDI_CHANNEL,
    SMR_GRID_CC,
    IDLE_TICKS_PER_STEP,
    IDLE_TRAIL_LENGTH
)
from features.idleAnimation.idle_animation import IdleAnimation


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

class SnakeAlongTheBorder(IdleAnimation):
    def __init__(self):
        super().__init__()
        self._tick_count = 0
        self._head_pos = 0

    def _set_led(self, row, col, on):
        """Turn a single SMR grid LED on or off."""
        cc = SMR_GRID_CC[row][col]
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, 127 if on else 0)

    def on_start(self):
        self._tick_count = 0
        self._head_pos = 0

    def on_stop(self):
        self._tick_count = 0
        self._head_pos = 0
        for r, c in _OUTER_RING:
            self._set_led(r, c, False)

    def on_tick(self):
        if self._tick_count % IDLE_TICKS_PER_STEP == 0:
            # Turn off the trailing LED
            tail_pos = (self._head_pos - IDLE_TRAIL_LENGTH) % _RING_LEN
            tr, tc = _OUTER_RING[tail_pos]
            self._set_led(tr, tc, False)

            # Turn on the new head LED
            hr, hc = _OUTER_RING[self._head_pos]
            self._set_led(hr, hc, True)

            self._head_pos = (self._head_pos + 1) % _RING_LEN

        self._tick_count += 1

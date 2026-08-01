# ─────────────────────────────────────────────
# features/project_load.py – "Inside-out" LED
#     animation on the SMR grid when a project
#     is loaded
# ─────────────────────────────────────────────

import midi
from device import midiOutMsg

from config import (
    MIDI_CHANNEL,
    SMR_GRID_CC,
    LOAD_TICKS_PER_RING,
    LOAD_HOLD_TICKS,
    LOAD_RIPPLES,
)

# ── Pre-compute rings (inside → out) ─────────
# The grid is 3 rows × 8 cols.  The "center" is
# between columns 3-4 and row 1 (middle row).
# Distance from center is max(row_dist, col_dist)
# giving us concentric rectangular rings.

_NUM_ROWS = len(SMR_GRID_CC)       # 3
_NUM_COLS = len(SMR_GRID_CC[0])    # 8

_CENTER_ROW = (_NUM_ROWS - 1) / 2  # 1.0
_CENTER_COL = (_NUM_COLS - 1) / 2  # 3.5


def _build_rings():
    """Group every (row, col) into rings by Chebyshev
    distance from the grid centre."""
    cells_by_dist = {}
    for r in range(_NUM_ROWS):
        for c in range(_NUM_COLS):
            dist = max(abs(r - _CENTER_ROW), abs(c - _CENTER_COL))
            cells_by_dist.setdefault(dist, []).append((r, c))

    # Sort by distance so ring 0 = innermost
    rings = []
    for dist in sorted(cells_by_dist):
        rings.append(cells_by_dist[dist])
    return rings


_RINGS = _build_rings()
_NUM_RINGS = len(_RINGS)

# ── Animation state ──────────────────────────

_tick = 0           # current OnIdle tick counter
_active = False     # True while animation is running
_phase = 0          # 0 = expanding, 1 = holding, 2 = done
_ripple_count = 0   # how many ripples have completed


def _set_led(row, col, on):
    """Turn a single SMR grid LED on (127) or off (0)."""
    cc = SMR_GRID_CC[row][col]
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, 127 if on else 0)


def _all_off():
    """Turn off every LED in the SMR grid."""
    for r in range(_NUM_ROWS):
        for c in range(_NUM_COLS):
            _set_led(r, c, False)


# ── Public API ────────────────────────────────

def start():
    """Trigger the inside-out animation.
    Call this from OnProjectLoad."""
    global _tick, _active, _phase, _ripple_count
    _all_off()
    _tick = 0
    _phase = 0
    _ripple_count = 0
    _active = True


def tick():
    """Advance the animation by one frame.
    Call this from OnIdle.  Returns True while the
    animation is still running (so the caller can
    skip other idle work if desired)."""
    global _tick, _active, _phase, _ripple_count

    if not _active:
        return False

    if _phase == 0:
        # ── Sweep phase ─────────────────────
        # The wave front lights rings 0→4, while
        # a trailing edge turns off rings 2 behind.
        # We keep going past _NUM_RINGS so the trail
        # finishes sweeping off the outer rings.
        _TRAIL = 2
        ring_index = _tick // LOAD_TICKS_PER_RING

        if ring_index < _NUM_RINGS + _TRAIL:
            if _tick % LOAD_TICKS_PER_RING == 0:
                # Light the next ring (if still in range)
                if ring_index < _NUM_RINGS:
                    for r, c in _RINGS[ring_index]:
                        _set_led(r, c, True)
                # Turn off the trailing ring
                tail = ring_index - _TRAIL
                if tail >= 0:
                    for r, c in _RINGS[tail]:
                        _set_led(r, c, False)
        else:
            # Wave has fully swept
            _ripple_count += 1
            if _ripple_count < LOAD_RIPPLES:
                # Start next ripple
                _tick = 0
                return True
            else:
                # Animation fully completely
                _active = False
                _phase = 2
                return False

    _tick += 1
    return True

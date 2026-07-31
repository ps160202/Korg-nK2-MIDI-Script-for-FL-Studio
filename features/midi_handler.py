# ─────────────────────────────────────────────
# features/midi_handler.py – Incoming MIDI
#     message router
# ─────────────────────────────────────────────

import transport
import midi
from device import midiOutMsg

from config import (
    MIDI_CHANNEL,
    PLAY_CC,
    STOP_CC,
    REW_CC,
    FF_CC,
    RECORD_CC,
)


def _echo_cc(cc, value):
    """Mirror a CC value back to the controller (LED feedback)."""
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, value)


# ── Individual button handlers ────────────────

def _handle_play(event):
    if event.data2 > 0:
        transport.start()
    event.handled = True


def _handle_record(event):
    if event.data2 > 0:
        transport.record()
    event.handled = True


def _handle_stop(event):
    _echo_cc(STOP_CC, event.data2)
    if event.data2 > 0:
        transport.stop()
    event.handled = True


def _handle_rewind(event):
    _echo_cc(REW_CC, event.data2)
    if event.data2 > 0:
        transport.rewind(2)
    else:
        transport.rewind(0)
    event.handled = True


def _handle_fast_forward(event):
    _echo_cc(FF_CC, event.data2)
    if event.data2 > 0:
        transport.fastForward(2)
    else:
        transport.fastForward(0)
    event.handled = True


# ── Dispatch table ────────────────────────────

_DISPATCH = {
    PLAY_CC:   _handle_play,
    RECORD_CC: _handle_record,
    STOP_CC:   _handle_stop,
    REW_CC:    _handle_rewind,
    FF_CC:     _handle_fast_forward,
}


def dispatch(event):
    """Route an incoming MIDI event to the correct handler.

    Returns without marking the event as handled if no mapping exists,
    so FL Studio can process it normally.
    """
    handler = _DISPATCH.get(event.data1)
    if handler:
        handler(event)
    else:
        event.handled = False

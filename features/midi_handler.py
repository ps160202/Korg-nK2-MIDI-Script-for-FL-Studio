# ─────────────────────────────────────────────
# features/midi_handler.py – Incoming MIDI
#     message router
# ─────────────────────────────────────────────

import transport
import midi
import channels
from device import midiOutMsg

from config import (
    MIDI_CHANNEL,
    PLAY_CC,
    STOP_CC,
    REW_CC,
    FF_CC,
    RECORD_CC,
    CYCLE_CC,
    SOLO_CC,
    MUTE_CC
)


def _echo_cc(cc, value):
    """Mirror a CC value back to the controller (LED feedback)."""
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, value)


# ── Individual button handlers ────────────────

def _handle_play(event):
    if event.data2 > 0:
        transport.start()

def _handle_record(event):
    if event.data2 > 0:
        transport.record()

def _handle_stop(event):
    _echo_cc(STOP_CC, event.data2)
    if event.data2 > 0:
        transport.stop()

def _handle_rewind(event):
    _echo_cc(REW_CC, event.data2)
    if event.data2 > 0:
        transport.rewind(2)
    else:
        transport.rewind(0)

def _handle_fast_forward(event):
    _echo_cc(FF_CC, event.data2)
    if event.data2 > 0:
        transport.fastForward(2)
    else:
        transport.fastForward(0)


def _handle_cycle(event):
    if event.data2 > 0:
        transport.setLoopMode()
        _echo_cc(CYCLE_CC, 127 if transport.getLoopMode() else 0)

def _handle_solo(event):
    if event.data2 > 0:
        selectedChannel = channels.selectedChannel(0)
        channels.soloChannel(selectedChannel)
        _echo_cc(SOLO_CC, 127 if channels.isChannelSolo(selectedChannel) else 0)

def _handle_mute(event):
    if event.data2 > 0:
        selectedChannel = channels.selectedChannel(0)
        channels.muteChannel(selectedChannel)
        _echo_cc(MUTE_CC, 127 if channels.isChannelMuted(selectedChannel) else 0)


# ── Dispatch table ────────────────────────────

_DISPATCH = {
    PLAY_CC:   _handle_play,
    RECORD_CC: _handle_record,
    STOP_CC:   _handle_stop,
    REW_CC:    _handle_rewind,
    FF_CC:     _handle_fast_forward,
    CYCLE_CC:  _handle_cycle,
    SOLO_CC:   _handle_solo,
    MUTE_CC:   _handle_mute,
}


def dispatch(event):
    """Route an incoming MIDI event to the correct handler.

    Returns without marking the event as handled if no mapping exists,
    so FL Studio can process it normally.
    """
    handler = _DISPATCH.get(event.data1)
    if handler:
        handler(event)
        event.handled = True
    else:
        event.handled = False

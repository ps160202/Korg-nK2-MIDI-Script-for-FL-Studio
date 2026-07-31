# ─────────────────────────────────────────────
# features/transport_leds.py – Sync controller
#     LEDs with FL Studio transport state
# ─────────────────────────────────────────────

import transport
import midi
from device import midiOutMsg

from config import MIDI_CHANNEL, PLAY_CC, RECORD_CC, CYCLE_CC


def update():
    """Send CC messages to mirror the current play/record state on the
    controller's transport LEDs."""

    # Play LED
    play_val = 127 if transport.isPlaying() else 0
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, PLAY_CC, play_val)

    # Record LED
    rec_val = 127 if transport.isRecording() else 0
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, RECORD_CC, rec_val)

    # Cycle LED (Song = ON, Pattern = OFF)
    cycle_val = 127 if transport.getLoopMode() else 0
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, CYCLE_CC, cycle_val)

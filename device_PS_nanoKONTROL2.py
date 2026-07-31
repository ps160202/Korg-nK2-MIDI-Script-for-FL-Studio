# name=PS nanoKONTROL2
# supportedDevices=nanoKONTROL2
# ─────────────────────────────────────────────
# device_PS_nanoKONTROL2.py
# Entry point — FL Studio MIDI script callbacks
# ─────────────────────────────────────────────

import midi

from features import transport_leds
from features import vu_meter
from features import midi_handler


def OnInit():
    """Called once when FL Studio loads the script."""
    transport_leds.update()


def OnRefresh(flags):
    """Called when FL Studio's internal state changes."""
    if flags & midi.HW_Dirty_LEDs:
        transport_leds.update()


def OnIdle():
    """Called continuously — drives the VU meter LEDs."""
    vu_meter.update()


def OnMidiMsg(event):
    """Called for every incoming MIDI message from the controller."""
    midi_handler.dispatch(event)
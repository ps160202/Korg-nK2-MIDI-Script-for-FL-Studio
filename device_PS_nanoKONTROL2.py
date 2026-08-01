# name=PS nanoKONTROL2
# supportedDevices=nanoKONTROL2
# ─────────────────────────────────────────────
# device_PS_nanoKONTROL2.py
# Entry point — FL Studio MIDI script callbacks
# ─────────────────────────────────────────────

from features.channel_SM_leds import set_SM_leds
import midi

from features import transport_leds
from features import vu_meter
from features import midi_handler
from features import project_load
from features import idle_animation
from features import channel_SM_leds


def OnInit():
    """Called once when FL Studio loads the script."""
    transport_leds.update()
    channel_SM_leds.set_SM_leds()

def OnRefresh(flags):
    """Called when FL Studio's internal state changes."""
    if flags & midi.HW_Dirty_LEDs:
        idle_animation.notify_activity()
        transport_leds.update()
    if flags & midi.HW_ChannelEvent:
        idle_animation.notify_activity()
        channel_SM_leds.set_SM_leds()


def OnProjectLoad(status):
    """Called when a project starts or finishes loading."""
    if status == 100:
        project_load.start()
        idle_animation.notify_activity()


def OnIdle():
    """Called continuously — drives animations and VU meters."""
    if project_load.tick():
        return
    if idle_animation.tick():
        return

    vu_meter.update()


def OnMidiMsg(event):
    """Called for every incoming MIDI message from the controller."""
    idle_animation.notify_activity()
    midi_handler.dispatch(event)
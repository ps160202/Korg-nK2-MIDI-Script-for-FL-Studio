# name=PS nanoKONTROL2
# supportedDevices=nanoKONTROL2
# ─────────────────────────────────────────────
# device_PS_nanoKONTROL2.py
# Entry point — FL Studio MIDI script callbacks
# ─────────────────────────────────────────────

import led_utils
from features.channel_SM_leds import set_SM_leds
import midi

from features import transport_leds
from features import vu_meter
from features import midi_handler
from features import project_load
from features import idleAnimation
from features import channel_SM_leds

_was_idle_anim_active = False


def OnInit():
    """Called once when FL Studio loads the script."""
    led_utils.turnOffAllLEDs()

    transport_leds.update()
    channel_SM_leds.set_SM_leds()

def OnRefresh(flags):
    """Called when FL Studio's internal state changes."""

    if flags & midi.HW_Dirty_LEDs:
        idleAnimation.notify_activity()
        transport_leds.update()
    
    channel_SM_leds.set_SM_leds()


def OnProjectLoad(status):
    """Called when a project starts or finishes loading."""
    if status == 100:
        project_load.start()
        idleAnimation.notify_activity()


def OnIdle():
    """Called continuously — drives animations and VU meters."""
    global _was_idle_anim_active

    if project_load.tick():
        return
    
    is_animating = idleAnimation.tick()
    if is_animating:
        _was_idle_anim_active = True
        return

    # If the animation just finished, force the cache to flush to the hardware
    if _was_idle_anim_active:
        channel_SM_leds.force_sync()
        channel_SM_leds.set_SM_leds()
        _was_idle_anim_active = False

    vu_meter.update()


def OnMidiMsg(event):
    """Called for every incoming MIDI message from the controller."""
    idleAnimation.notify_activity()
    midi_handler.dispatch(event)
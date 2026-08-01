from config import MUTE_CC, SOLO_CC
from features.midi_handler import _echo_cc
import channels

def set_SM_leds():
    selected_channel = channels.selectedChannel(0)

    # Solo
    if channels.isChannelSolo(selected_channel):
        _echo_cc(SOLO_CC, 127)
    else:
        _echo_cc(SOLO_CC, 0)

    # Mute
    if channels.isChannelMuted(selected_channel):
        _echo_cc(MUTE_CC, 127)
    else:
        _echo_cc(MUTE_CC, 0)
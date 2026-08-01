from config import MUTE_CC, SOLO_CC
from features.midi_handler import _echo_cc
import channels

_last_solo = None
_last_mute = None
_last_selected = None
_force_sync = True

def force_sync():
    global _force_sync
    _force_sync = True

def set_SM_leds():
    global _last_solo, _last_mute, _last_selected, _force_sync
    
    selected_channel = channels.selectedChannel(0)
    isSolo = channels.isChannelSolo(selected_channel)
    isMute = channels.isChannelMuted(selected_channel)

    if _force_sync or isSolo != _last_solo or isMute != _last_mute or selected_channel != _last_selected:
        _last_solo = isSolo
        _last_mute = isMute
        _last_selected = selected_channel
        _force_sync = False
        
        # Solo
        if isSolo:
            _echo_cc(SOLO_CC, 127)
        else:
            _echo_cc(SOLO_CC, 0)

        # Mute
        if isMute:
            _echo_cc(MUTE_CC, 127)
        else:
            _echo_cc(MUTE_CC, 0)
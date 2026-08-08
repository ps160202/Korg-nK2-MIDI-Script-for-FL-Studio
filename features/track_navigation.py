# ─────────────────────────────────────────────
# features/track_navigation.py – Track prev/next
#     and piano roll/plugin editor toggling
# ─────────────────────────────────────────────

import channels
import midi
import ui
from enum import IntEnum
from config import FORCE_CLOSE_PLUGIN_ON_TRACK_CHANGE

class EditorState(IntEnum):
    CLOSED     = 0
    PIANO_ROLL = 1
    PLUGIN     = 2

_editor_state = EditorState.CLOSED

def open_piano_roll_for_channel(channel):
    eventId = channels.getRecEventId(channel) + midi.REC_Chan_PianoRoll
    ui.openEventEditor(eventId, midi.EE_PR)

def _refresh_piano_roll():
    """Refresh open editors for the newly selected channel."""
    newChannel = channels.selectedChannel(0)
    if ui.getVisible(midi.widPianoRoll):
        open_piano_roll_for_channel(newChannel)
    if _editor_state == EditorState.PLUGIN:
        channels.showEditor(newChannel, 1)        # force-open new plugin

def handle_track_prev(event):
    if event.data2 > 0:
        oldChannel = channels.selectedChannel(0)
        if FORCE_CLOSE_PLUGIN_ON_TRACK_CHANGE:
            channels.showEditor(oldChannel, 0)        # force-close old plugin
        newChannel = (oldChannel - 1) % channels.channelCount()
        channels.selectOneChannel(newChannel)
        _refresh_piano_roll()

def handle_track_next(event):
    if event.data2 > 0:
        oldChannel = channels.selectedChannel(0)
        if FORCE_CLOSE_PLUGIN_ON_TRACK_CHANGE:
            channels.showEditor(oldChannel, 0)        # force-close old plugin
        newChannel = (oldChannel + 1) % channels.channelCount()
        channels.selectOneChannel(newChannel)
        _refresh_piano_roll()

def handle_pianoroll_plugin_toggle(event):
    """Cycle: 1st click → open piano roll, 2nd → close PR & open plugin, 3rd → close plugin."""
    global _editor_state
    if event.data2 > 0:
        ch = channels.selectedChannel(0)
        if _editor_state == EditorState.CLOSED:
            # Open piano roll
            open_piano_roll_for_channel(ch)
            _editor_state = EditorState.PIANO_ROLL
        elif _editor_state == EditorState.PIANO_ROLL:
            # Close piano roll, open plugin
            ui.hideWindow(midi.widPianoRoll)
            channels.showEditor(ch)
            _editor_state = EditorState.PLUGIN
        else:
            # Close plugin
            channels.showEditor(ch)
            _editor_state = EditorState.CLOSED

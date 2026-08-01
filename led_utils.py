from config import (
    MIDI_CHANNEL,
    PLAY_CC,
    STOP_CC,
    REW_CC,
    FF_CC,
    RECORD_CC,
    CYCLE_CC,
    SMR_GRID_CC,
)
from device import midiOutMsg
import midi


def turnOffAllLEDs():
    for row in SMR_GRID_CC:
        for cc in row:
            midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, 0)

    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, PLAY_CC, 0)
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, STOP_CC, 0)
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, REW_CC, 0)
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, FF_CC, 0)
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, RECORD_CC, 0)
    midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, CYCLE_CC, 0)    

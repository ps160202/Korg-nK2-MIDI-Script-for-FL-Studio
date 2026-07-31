# name=PS nanoKONTROL2
# supportedDevices=nanoKONTROL2

import transport
import midi
from device import midiOutMsg

import mixer

SMR_R = [39, 38, 37, 36, 35, 34, 33, 32]
SMR_L = [55, 54, 53, 52, 51, 50, 49, 48]

def OnIdle():

    peak_R = mixer.getLastPeakVol(0)
    peak_L = mixer.getLastPeakVol(1)

    leds_R = min(8, int(peak_R * 10))
    leds_L = min(8, int(peak_L * 10))

    for i, cc in enumerate(SMR_R):
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            cc,
            127 if i < leds_R else 0
        )

    for i, cc in enumerate(SMR_L):
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            cc,
            127 if i < leds_L else 0
        )

PLAY_CC   = 41
STOP_CC   = 42
REW_CC    = 43
FF_CC     = 44
RECORD_CC = 45

# nanoKONTROL2 uses zero-based MIDI channels.
# Channel 0 = MIDI Channel 1
MIDI_CHANNEL = 0


def updateTransportLEDs():
    """Synchronize controller LEDs with FL Studio transport."""

    # Play LED
    if transport.isPlaying():
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, PLAY_CC, 127)
    else:
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, PLAY_CC, 0)

    # Record LED
    if transport.isRecording():
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, RECORD_CC, 127)
    else:
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, RECORD_CC, 0)


def OnInit():
    updateTransportLEDs()


def OnRefresh(flags):
    if flags & midi.HW_Dirty_LEDs:
        updateTransportLEDs()


def OnMidiMsg(event):

    # PLAY
    if event.data1 == PLAY_CC:
        if event.data2 > 0:
            transport.start()

        event.handled = True
        return

    # RECORD
    if event.data1 == RECORD_CC:
        if event.data2 > 0:
            transport.record()

        event.handled = True
        return

    # STOP
    if event.data1 == STOP_CC:
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            STOP_CC,
            event.data2
        )

        if event.data2 > 0:
            transport.stop()

        event.handled = True
        return


    # REWIND
    if event.data1 == REW_CC:
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            REW_CC,
            event.data2
        )

        if event.data2 > 0:
            transport.rewind(2)
        else:
            transport.rewind(0)

        event.handled = True
        return


    # FAST FORWARD
    if event.data1 == FF_CC:
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            FF_CC,
            event.data2
        )

        if event.data2 > 0:
            transport.fastForward(2)
        else:
            transport.fastForward(0)

        event.handled = True
        return

    # Pass everything else through
    event.handled = False
# ─────────────────────────────────────────────
# features/vu_meter.py – VU / peak-meter
#     visualisation on the Solo & Mute button LEDs
# ─────────────────────────────────────────────

import midi
import mixer
from device import midiOutMsg

from config import MIDI_CHANNEL, VU_RIGHT_CCS, VU_LEFT_CCS


def update():
    """Read master-channel peak levels and drive the S/M button LEDs
    as a simple stereo VU meter."""

    peak_r = mixer.getLastPeakVol(0)
    peak_l = mixer.getLastPeakVol(1)

    leds_r = min(8, int(peak_r * 10))
    leds_l = min(8, int(peak_l * 10))

    for i, cc in enumerate(VU_RIGHT_CCS):
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            cc,
            127 if i < leds_r else 0,
        )

    for i, cc in enumerate(VU_LEFT_CCS):
        midiOutMsg(
            midi.MIDI_CONTROLCHANGE,
            MIDI_CHANNEL,
            cc,
            127 if i < leds_l else 0,
        )

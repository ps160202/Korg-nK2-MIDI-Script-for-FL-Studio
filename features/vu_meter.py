# ─────────────────────────────────────────────
# features/vu_meter.py – VU / peak-meter
#     visualisation on the Solo & Mute button LEDs
# ─────────────────────────────────────────────

import midi
import mixer
from device import midiOutMsg

from config import MIDI_CHANNEL, VU_RIGHT_CCS, VU_LEFT_CCS, VU_SENSITIVITY


def update():
    """Read master-channel peak levels and drive the S/M button LEDs
    as a simple stereo VU meter."""

    peak_l = mixer.getLastPeakVol(0)
    peak_r = mixer.getLastPeakVol(1)

    num_leds = len(VU_RIGHT_CCS)
    leds_l = min(num_leds, int(peak_l * (num_leds * VU_SENSITIVITY)))
    leds_r = min(num_leds, int(peak_r * (num_leds * VU_SENSITIVITY)))

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

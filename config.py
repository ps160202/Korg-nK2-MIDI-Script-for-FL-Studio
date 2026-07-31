# ─────────────────────────────────────────────
# config.py – Constants & CC mappings
# ─────────────────────────────────────────────

# nanoKONTROL2 uses zero-based MIDI channels.
# Channel 0 = MIDI Channel 1
MIDI_CHANNEL = 0

# ── Transport button CCs ──────────────────────
PLAY_CC   = 41
STOP_CC   = 42
REW_CC    = 43
FF_CC     = 44
RECORD_CC = 45

# ── Solo / Mute / Record-arm LED CCs (VU meter) ─
# Right channel (mapped to S buttons, descending)
VU_RIGHT_CCS = [39, 38, 37, 36, 35, 34, 33, 32]
# Left channel  (mapped to M buttons, descending)
VU_LEFT_CCS  = [55, 54, 53, 52, 51, 50, 49, 48]
# Sensitivity of VU meter. Range from 0 to 2 (1 being default sensitivity)
VU_Sensitivity = 1.2

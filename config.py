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
CYCLE_CC  = 46

# ── SMR Grid CCs ─────────────────────────────
SMR_GRID_CC = [
    [32, 33, 34, 35, 36, 37, 38, 39],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [64, 65, 66, 67, 68, 69, 70, 71]
]

# -- Solo / Mute Current Track ---
SOLO_CC = SMR_GRID_CC[0][0]
MUTE_CC = SMR_GRID_CC[1][0]

# ── Solo / Mute / Record-arm LED CCs (VU meter) ─
# Right channel (mapped to S buttons, descending). Exclude column 0 used for Solo.
VU_RIGHT_CCS = SMR_GRID_CC[0][1:][::-1]
# Left channel  (mapped to M buttons, descending). Exclude column 0 used for Mute.
VU_LEFT_CCS  = SMR_GRID_CC[1][1:][::-1]
# Sensitivity of VU meter. Range from 0 to 2 (1 being default sensitivity)
VU_SENSITIVITY = 1

# ── Project-load animation ───────────────────
# Delay between each ring (in OnIdle ticks).
# FL Studio calls OnIdle roughly every ~20-30 ms,
# so 8 ticks ≈ 160-240 ms per ring.
LOAD_TICKS_PER_RING = 8

# How long to hold all LEDs on at the end before
# turning them off (in ticks).
LOAD_HOLD_TICKS = 100

# Number of times the inside-out ripple effect should play
LOAD_RIPPLES = 2

# Number of rings before the trailing edge turns them off
LOAD_TRAIL_LENGTH = 2

# ── Idle Animation ─────────────────────────────
# Seconds of no MIDI messages before animation starts
IDLE_TIMEOUT_SEC = 5.0
# Animation speed (OnIdle ticks per step)
IDLE_TICKS_PER_STEP = 12
# Number of LEDs in the trail
IDLE_TRAIL_LENGTH = 3

from features.idleAnimation.idle_animation import IdleAnimation
from config import (
    MIDI_CHANNEL,
    SMR_GRID_CC,
    IDLE_TICKS_PER_STEP,
    IDLE_TRAIL_LENGTH
)
from device import midiOutMsg
import midi

_NUM_COLS = len(SMR_GRID_CC[0])
_NUM_ROWS = len(SMR_GRID_CC)

class BarberPole(IdleAnimation):
    def __init__(self):
        super().__init__()
        self._tick_count = 0
        self.heads = []

    def _set_led(self, row, col, on):
        """Turn a single SMR grid LED on or off."""
        cc = SMR_GRID_CC[row][col]
        midiOutMsg(midi.MIDI_CONTROLCHANGE, MIDI_CHANNEL, cc, 127 if on else 0)

    def on_start(self):
        self._tick_count = 0
        # Cascade initial column positions (e.g., 0, -1, -2) backwards per row
        self.heads = [-i for i in range(_NUM_ROWS)]

    def on_stop(self):
        self._tick_count = 0
        for r in range(_NUM_ROWS):
            for c in range(_NUM_COLS):
                self._set_led(r, c, False)

    def on_tick(self):
        if self._tick_count % IDLE_TICKS_PER_STEP == 0:
            for r in range(_NUM_ROWS):
                # Increment the absolute position
                self.heads[r] += 1
                curr_head = self.heads[r]
                
                # Turn off the trailing LED if it has visibly entered the board
                tail = curr_head - IDLE_TRAIL_LENGTH
                if tail >= 0:
                    self._set_led(r, tail % _NUM_COLS, False)

                # Turn on the new head LED if it has visibly entered the board
                if curr_head >= 0:
                    self._set_led(r, curr_head % _NUM_COLS, True)

        self._tick_count += 1
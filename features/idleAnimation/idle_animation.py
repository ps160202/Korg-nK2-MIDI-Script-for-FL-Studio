import time
import transport
import mixer

from config import IDLE_TIMEOUT_SEC

class IdleAnimation:
    def __init__(self):
        self._last_activity = time.time()
        self._active = False

    def notify_activity(self):
        """Reset the idle timer. Call this on any controller action."""
        self._last_activity = time.time()
        if self._active:
            self.stop()

    def stop(self):
        """Stop animation and clear LEDs."""
        self._active = False
        self.on_stop()

    def on_stop(self):
        """Override to clear LEDs."""
        pass

    def tick(self):
        """Advance the animation if idle."""
        # If the track is playing or audio is passing through the master mixer, we are not idle.
        if transport.isPlaying() or mixer.getLastPeakVol(0) > 0.005 or mixer.getLastPeakVol(1) > 0.005:
            self.notify_activity()
            return False

        if not self._active:
            if time.time() - self._last_activity >= IDLE_TIMEOUT_SEC:
                # Become active
                self._active = True
                self.on_start()
            else:
                return False

        self.on_tick()
        return True

    def on_start(self):
        """Called when idle mode starts."""
        pass

    def on_tick(self):
        """Implement logic for ticking the animation."""
        pass

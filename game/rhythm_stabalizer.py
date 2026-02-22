import collections

class RhythmSyncStabilizer:
    def __init__(self, window_size=8, correction_gain=0.10):
        self.error_window = collections.deque(maxlen=window_size)
        self.gain = correction_gain

        self.filtered_error = 0

    def update(self, audio_time_ms, predicted_time_ms):
        error = audio_time_ms - predicted_time_ms

        self.error_window.append(error)

        # Moving average phase filter
        self.filtered_error = sum(self.error_window) / len(self.error_window)

        return predicted_time_ms + self.gain * self.filtered_error
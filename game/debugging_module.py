import numpy as np

class TimingProfiler:
    def __init__(self):
        self.samples = []
        self.max_samples = 10000

    def record(self, audio_time, game_time):
        if len(self.samples) >= self.max_samples:
            return

        self.samples.append((audio_time, game_time))

    def analyze(self):
        import statistics

        if not self.samples:
            return

        errors = [abs(a - g) for a, g in self.samples]

        print("=== TIMING PROFILER REPORT ===")
        print(f"Samples: {len(errors)}")
        print(f"Mean Drift: {statistics.mean(errors):.3f} ms")
        print(f"Max Drift: {max(errors):.3f} ms")
        print(f"Min Drift: {min(errors):.3f} ms")



    def detect_trend(self):
        import numpy as np

        if len(self.samples) < 5:
            print("Not enough samples to detect trend")
            return

        samples = self.samples

        x = np.arange(len(samples))
        y = np.array([abs(a-b) for a,b in samples])

        slope = np.polyfit(x, y, 1)[0]

        if abs(slope) < 0.001:
            print("Drift is NOT gradual")
        else:
            print("Gradual drift detected")
            print("Drift growth rate:", slope)
    def detect_threshold_break(self):
        THRESHOLD = 40  # ms

        for i, (a, g) in enumerate(self.samples):
            if abs(a - g) > THRESHOLD:
                print("Drift first exceeds threshold at sample index:", i)
                break
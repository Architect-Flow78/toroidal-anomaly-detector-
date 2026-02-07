
# torus.py
import numpy as np

class MultiPhaseTorus:
    def __init__(self, phase_bins=48, decay=0.995):
        self.phase_bins = phase_bins
        self.decay = decay

        self.fields = {
            "direction": np.zeros(phase_bins),
            "speed": np.zeros(phase_bins),
            "curvature": np.zeros(phase_bins),
        }

        self.prev_x = None
        self.prev_dx = None

    def _phase(self, v):
        angle = np.arctan2(v, 1.0)
        idx = int(((angle + np.pi) / (2 * np.pi)) * self.phase_bins)
        return idx % self.phase_bins

    def step(self, x):
        if self.prev_x is None:
            self.prev_x = x
            return None

        dx = x - self.prev_x
        self.prev_x = x

        speed = np.linalg.norm(dx)
        if speed == 0:
            return self._victim("застой энергии", 10.0)

        direction = dx / speed
        curvature = 0 if self.prev_dx is None else np.linalg.norm(dx - self.prev_dx)
        self.prev_dx = dx

        phases = {
            "direction": self._phase(direction[0]),
            "speed": self._phase(speed),
            "curvature": self._phase(curvature),
        }

        for k in self.fields:
            self.fields[k] *= self.decay
            self.fields[k][phases[k]] += 1.0

        return self._analyze()

    def _analyze(self):
        ratios = []
        for field in self.fields.values():
            mean = np.mean(field) + 1e-6
            ratios.append(np.max(field) / mean)

        score = max(ratios)

        if score > 6.0:
            return self._victim("резонанс фаз", score)

        return {
            "mode": "ТВОРЕЦ",
            "anomaly_score": score
        }

    def _victim(self, reason, score):
        return {
            "mode": "ЖЕРТВА",
            "reason": reason,
            "anomaly_score": score
        }

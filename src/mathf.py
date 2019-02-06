from math import *

class Mathf:
    @staticmethod
    def clamp01(value):
        if value < 0.0: return 0.0
        if value > 1.0: return 1.0
        return value

    def clamp(value, min, max):
        if value < min: return min
        if value > max: return max
        return value

    def lerp(a, b, t):
        return a + (b - a) * Mathf.clamp01(t)

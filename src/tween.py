from math import *

class Tween:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.duration = 0
        self.elapsed = 0

        self.current = 0
        self.delta = 0
        self.done = True

    def tween(self, begin, end, duration):
        self.begin = begin
        self.end = end
        self.duration = duration
        self.current = begin
        self.change = 0
        self.elapsed = 0
        self.done = False

    def is_done(self):
        return self.done

    def get_current(self):
        return self.current

    def get_delta(self):
        return self.delta

    def update(self, elapsed_time):
        if self.done == True:
            return
        self.elapsed += elapsed_time
        if self.elapsed > self.duration:
            self.elapsed = self.duration
            self.done = True

        value = self.ease_in_sine(self.elapsed, self.begin, self.end, self.duration)
        self.delta = value - self.current
        self.current = value

    # -c * math.cos(t/d * (math.pi/2)) + c + b
    def ease_in_sine(self, elapsed, begin, end, duration):
        change = end - begin
        return -change * cos(elapsed/duration * (pi/2)) + change + begin


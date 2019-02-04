# Using Robert Penner' easing functions
# http://robertpenner.com/easing
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

        # foo = self.ease_in_sine
        # foo = self.ease_in_quad
        # foo = self.ease_in_cubic
        # foo = self.ease_in_circ
        foo = self.ease_cosine
        value = foo(self.elapsed, self.begin, self.end, self.duration)
        self.delta = value - self.current
        self.current = value

    # -c * cos(t/d * (pi/2)) + c + b
    def ease_in_sine(self, elapsed, begin, end, duration):
        change = end - begin
        value = elapsed / duration
        return -change * cos(value * (pi/2)) + change + begin

    def ease_in_quad(self, elapsed, begin, end, duration):
        change = end - begin
        value = elapsed / duration
        return end * value * value + begin

    def ease_in_cubic(self, elapsed, begin, end, duration):
        change = end - begin
        value = elapsed / duration
        return change * value * value * value + begin

    def ease_in_circ(self, elapsed, begin, end, duration):
        change = end - begin
        value = elapsed / duration
        return -change * (sqrt(1 - value * value) - 1) + begin

    def ease_cosine(self, elapsed, begin, end, duration):
        value = elapsed / duration
        t = (1.0 - cos(value * pi)) / 2.0
        return begin * (1.0 - t) + end * t

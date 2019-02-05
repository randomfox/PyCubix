# Using Robert Penner' easing functions
# http://robertpenner.com/easing
from enum import Enum
from math import *

class TweenEaseType(Enum):
    EASE_COSINE = 0
    EASE_IN_SINE = 1
    EASE_IN_QUAD = 2
    EASE_IN_CUBIC = 3
    EASE_IN_CIRC = 4

class Tween:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.duration = 0
        self.elapsed = 0

        self.current = 0
        self.delta = 0
        self.done = True

        self.ease_type = TweenEaseType.EASE_COSINE
        self.ease_foo = self.ease_cosine

    def tween(self, begin, end, duration, ease_type=TweenEaseType.EASE_COSINE):
        self.begin = begin
        self.end = end
        self.duration = duration
        self.current = begin
        self.change = 0
        self.elapsed = 0
        self.done = False
        self.ease_foo = self.get_ease_func(ease_type)

    def get_ease_func(self, type):
        if type == TweenEaseType.EASE_IN_SINE:
            return self.ease_in_sine
        elif type == TweenEaseType.EASE_IN_QUAD:
            return self.ease_in_quad
        elif type == TweenEaseType.EASE_IN_CUBIC:
            return self.ease_in_cubic
        elif type == TweenEaseType.EASE_IN_CIRC:
            return self.ease_in_circ
        else:
            return self.ease_cosine

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

        value = self.ease_foo(self.elapsed, self.begin, self.end, self.duration)
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

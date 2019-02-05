# Using Robert Penner' easing functions
# http://robertpenner.com/easing
from enum import Enum
from math import *

class TweenEaseType(Enum):
    EASE_COSINE = 0
    EASE_IN_SINE = 1
    EASE_OUT_SINE = 2
    EASE_IN_OUT_SINE = 3
    EASE_IN_QUAD = 4
    EASE_OUT_QUAD = 5
    EASE_IN_OUT_QUAD = 6
    EASE_IN_CUBIC = 7
    EASE_OUT_CUBIC = 8
    EASE_IN_OUT_CUBIC = 9

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
        if type == TweenEaseType.EASE_IN_SINE: return self.ease_in_sine
        if type == TweenEaseType.EASE_OUT_SINE: return self.ease_out_sine
        if type == TweenEaseType.EASE_IN_OUT_SINE: return self.ease_in_out_sine
        if type == TweenEaseType.EASE_IN_QUAD: return self.ease_in_quad
        if type == TweenEaseType.EASE_OUT_QUAD: return self.ease_out_quad
        if type == TweenEaseType.EASE_IN_OUT_QUAD: return self.ease_in_out_quad
        if type == TweenEaseType.EASE_IN_CUBIC: return self.ease_in_cubic
        if type == TweenEaseType.EASE_OUT_CUBIC: return self.ease_out_cubic
        if type == TweenEaseType.EASE_IN_OUT_CUBIC: return self.ease_in_out_cubic
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

        value = self.elapsed / self.duration
        value = self.ease_foo(self.begin, self.end, value)
        self.delta = value - self.current
        self.current = value

    def ease_in_sine(self, begin, end, value):
        change = end - begin
        return -change * cos(value * (pi/2)) + change + begin

    def ease_out_sine(self, begin, end, value):
        change = end - begin
        return change * sin(value * (pi/2)) + begin

    def ease_in_out_sine(self, begin, end, value):
        change = end - begin
        return change * sin(value * (pi/2)) + begin

    def ease_in_quad(self, begin, end, value):
        change = end - begin
        return change * value * value + begin

    def ease_out_quad(self, begin, end, value):
        change = end - begin
        return -change * value * (value - 2.0) + begin

    def ease_in_out_quad(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1.0:
            return change * 0.5 * value * value + begin
        value -= 1.0
        return -change * 0.5 * (value * (value - 2.0) - 1.0) + begin;

    def ease_in_cubic(self, begin, end, value):
        change = end - begin
        return change * value * value * value + begin

    def ease_out_cubic(self, begin, end, value):
        change = end - begin
        value -= 1.0
        return change * (value * value * value + 1.0) + begin;

    def ease_in_out_cubic(self, begin, end, value):
        change = end - begin
        value /= 0.5
        if value < 1.0:
            return change * 0.5 * value * value * value + begin;
        value -= 2.0;
        return change * 0.5 * (value * value * value + 2.0) + begin;

    def ease_cosine(self, begin, end, value):
        t = (1.0 - cos(value * pi)) / 2.0
        return begin * (1.0 - t) + end * t

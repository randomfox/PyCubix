from enum import Enum

class Face(Enum):
    FRONT_CW = 1
    FRONT_CCW = -1
    BACK_CW = 2
    BACK_CCW = -2
    LEFT_CW = 3
    LEFT_CCW = -3
    RIGHT_CW = 4
    RIGHT_CCW = -4
    UP_CW = 5
    UP_CCW = -5
    DOWN_CW = 6
    DOWN_CCW = -6

class State(Enum):
    IDLE = 0
    TWEENING = 1

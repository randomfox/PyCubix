from enums import *

class Constants:
    WINDOW_CAPTION = 'PyCubix'

    KNOWN_NOTATIONS = [
        "F",
        "F'",
        "B",
        "B'",
        "U",
        "U'",
        "D",
        "D'",
        "L",
        "L'",
        "R",
        "R'"
    ]

    NOTATION_TO_FACE_ROTATION_MAP = {
        "F": FaceRotation.FRONT_CW,
        "F'": FaceRotation.FRONT_CCW,
        "B": FaceRotation.BACK_CW,
        "B'": FaceRotation.BACK_CCW,
        "U": FaceRotation.UP_CW,
        "U'": FaceRotation.UP_CCW,
        "D": FaceRotation.DOWN_CW,
        "D'": FaceRotation.DOWN_CCW,
        "L": FaceRotation.LEFT_CW,
        "L'": FaceRotation.LEFT_CCW,
        "R": FaceRotation.RIGHT_CW,
        "R'": FaceRotation.RIGHT_CCW
    }

    FACE_ROTATION_TO_NOTATION_MAP = {
        FaceRotation.FRONT_CW: "F",
        FaceRotation.FRONT_CCW: "F'",
        FaceRotation.BACK_CW: "B",
        FaceRotation.BACK_CCW: "B'",
        FaceRotation.UP_CW: "U",
        FaceRotation.UP_CCW: "U'",
        FaceRotation.DOWN_CW: "D",
        FaceRotation.DOWN_CCW: "D'",
        FaceRotation.LEFT_CW: "L",
        FaceRotation.LEFT_CCW:"L'",
        FaceRotation.RIGHT_CW: "R",
        FaceRotation.RIGHT_CCW: "R'"
    }

    CW_FACE_ROTATIONS = [
        FaceRotation.FRONT_CW,
        FaceRotation.BACK_CW,
        FaceRotation.LEFT_CW,
        FaceRotation.RIGHT_CW,
        FaceRotation.UP_CW,
        FaceRotation.DOWN_CW
    ]

    CCW_FACE_ROTATIONS = [
        FaceRotation.FRONT_CCW,
        FaceRotation.BACK_CCW,
        FaceRotation.LEFT_CCW,
        FaceRotation.RIGHT_CCW,
        FaceRotation.UP_CCW,
        FaceRotation.DOWN_CCW
    ]

    GEOMETRY_FACE_ORIENTATION_ORDER = [
        Face.FRONT,
        Face.LEFT,
        Face.BACK,
        Face.RIGHT,
        Face.UP,
        Face.DOWN
    ]

    STR_TO_FACE_MAP = {
        "FRONT": Face.FRONT,
        "LEFT": Face.LEFT,
        "BACK": Face.BACK,
        "RIGHT": Face.RIGHT,
        "UP": Face.UP,
        "DOWN": Face.DOWN
    }

    STR_TO_COLOR_MAP = {
        "BLUE": Color.BLUE,
        "ORANGE": Color.ORANGE,
        "GREEN": Color.GREEN,
        "RED": Color.RED,
        "YELLOW": Color.YELLOW,
        "WHITE": Color.WHITE
    }

    SEXY_MOVE_TRIGGER = "R U R' U'"
    SLEDGEHAMMER_TRIGGER = "R' F R F'"

    # pattern nicked from https://ruwix.com/the-rubiks-cube/rubiks-cube-patterns-algorithms/
    CHECKERBOARD_PATTERN = "U2 D2 F2 B2 L2 R2"
    CUBE_IN_CUBE_PATTERN = "F L F U' R U F2 L2 U' L' B D' B' L2 U"
    FOUR_CROSSES_PATTERN = "U2 R2 L2 F2 B2 D2 L2 R2 F2 B2"
    FOUR_SPOTS_PATTERN = "F2 B2 U D' R2 L2 U D'"
    PLUS_MINUS_PATTERN = "U2 R2 L2 U2 R2 L2"
    SIX_SPOTS_PATTERN = "U D' R L' F B' U D'"
    SUPERFLIP_PATTERN = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    TETRIS_PATTERN = "L R F B U' D' L' R'"
    VERTICAL_STRIPES_PATTERN = "F U F R L2 B D' R D2 L D' B R2 L F U F"

    BLUE_COLOR = (0.066, 0.490, 0.988)
    ORANGE_COLOR = (0.996, 0.549, 0.184)
    GREEN_COLOR = (0.102, 0.878, 0.133)
    RED_COLOR = (0.855, 0.082, 0.102)
    YELLOW_COLOR = (0.961, 1.000, 0.204)
    WHITE_COLOR = (1.000, 1.000, 1.000)

    COLOR_TO_COLOR_VALUE_MAP = {
        Color.BLUE: BLUE_COLOR,
        Color.ORANGE: ORANGE_COLOR,
        Color.GREEN: GREEN_COLOR,
        Color.RED: RED_COLOR,
        Color.YELLOW: YELLOW_COLOR,
        Color.WHITE: WHITE_COLOR
    }

    FACE_TO_COLOR_MAP = {
        Face.FRONT: Color.BLUE,
        Face.LEFT: Color.ORANGE,
        Face.BACK: Color.GREEN,
        Face.RIGHT: Color.RED,
        Face.UP: Color.YELLOW,
        Face.DOWN: Color.WHITE
    }

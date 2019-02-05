from enums import *

class Constants:
    PRIME = '\''

    KNOWN_NOTATIONS = [
        "F", "F'", "F2", "F2'",
        "B", "B'", "B2", "B2'",
        "L", "L'", "L2", "L2'",
        "R", "R'", "R2", "R2'",
        "U", "U'", "U2", "U2'",
        "D", "D'", "D2", "D2'",
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

    FACE_TO_NAME_MAP = {
        Face.FRONT: "front",
        Face.BACK: "back",
        Face.LEFT: "left",
        Face.RIGHT: "right",
        Face.UP: "up",
        Face.DOWN: "down"
    }

    NAME_TO_FACE_MAP = {
        "front": Face.FRONT,
        "left": Face.LEFT,
        "back": Face.BACK,
        "right": Face.RIGHT,
        "up": Face.UP,
        "down": Face.DOWN
    }

    SEXY_MOVE_TRIGGER = "R U R' U'"
    SLEDGEHAMMER_TRIGGER = "R' F R F'"

    # patterns nicked from https://ruwix.com/the-rubiks-cube/rubiks-cube-patterns-algorithms/
    CHECKERBOARD_PATTERN = "U2 D2 F2 B2 L2 R2"
    CUBE_IN_CUBE_PATTERN = "F L F U' R U F2 L2 U' L' B D' B' L2 U"
    FOUR_CROSSES_PATTERN = "U2 R2 L2 F2 B2 D2 L2 R2 F2 B2"
    FOUR_SPOTS_PATTERN = "F2 B2 U D' R2 L2 U D'"
    GIFT_BOX_PATTERN = "U B2 R2 B2 L2 F2 R2 D' F2 L2 B F' L F2 D U' R2 F' L' R'"
    HI_AGAIN_PATTERN = "U2 D2 L2 U2 D2 R2 F2 B2 L2 F2 B2 R2 U2 D2 F2 U2 D2 B2"
    HI_ALL_AROUND_PATTERN = "U2 R2 F2 U2 D2 F2 L2 U2"
    PLUS_MINUS_PATTERN = "U2 R2 L2 U2 R2 L2"
    SIX_SPOTS_PATTERN = "U D' R L' F B' U D'"
    SPEEDSOLVER_PATTERN = "R' L' U2 F2 D2 F2 R L B2 U2 B2 U2"
    SUPERFLIP_PATTERN = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    TETRIS_PATTERN = "L R F B U' D' L' R'"
    UNION_JACK_PATTERN = "U F B' L2 U2 L2 F' B U2 L2 U"
    VERTICAL_STRIPES_PATTERN = "F U F R L2 B D' R D2 L D' B R2 L F U F"
    WIRE_PATTERN = "R L F B R L F B R L F B R2 B2 L2 R2 B2 L2"

    FALLBACK_COLOR = (1, 0, 1)

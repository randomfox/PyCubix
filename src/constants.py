from enums import *

class Constants:
    PRIME = "'"
    FALLBACK_COLOR = (1, 0, 1)

    KNOWN_NOTATIONS = [
        "F", "F'", "F2", "F2'",
        "B", "B'", "B2", "B2'",
        "L", "L'", "L2", "L2'",
        "R", "R'", "R2", "R2'",
        "U", "U'", "U2", "U2'",
        "D", "D'", "D2", "D2'",
    ]
    ALL_NOTATIONS = [
        "F", "F'", "F2", # "F2'", don't need double prime moves
        "B", "B'", "B2", # "B2'", although I'll let it in it'll be
        "L", "L'", "L2", # "L2'", commented out
        "R", "R'", "R2", # "R2'",
        "U", "U'", "U2", # "U2'",
        "D", "D'", "D2", # "D2'",
        # Not yet implanted moves
        # Not adding wide moves (yet) because you can just do a turn on the other side
        # whole cube rotations
        "X", "X'", "X2",
        "Y", "Y'", "Y2",
        "Z", "Z'", "Z2",
        # Slice moves
        "M", "M'", "M2", # cutting through F vertically
        "E", "E'", "E2", # horizantal
        "S", "S'", "S2", # cutting through R vertically
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

    STATES = ['UNSOLVED', 'CROSS', 'F2L', 'OLL', 'PLL', 'SOLVED']

    # Algs all algs are from jperm.net
    # OLL
    OLL = [
        "R U2 R2 F R F' U2 R' F R F'", # Dot
        "r U r' U2 r U2 R' U2 R U' r'", # Dot
        "r' R2 U R' U r U2 r' U M'", # Dot
        "M U' r U2 r' U' R U' R' M'", # Dot
        "l' U2 L U L' U l", # Square Shape
        "r U2 R' U' R U' r'", # Square Shape
        "r U R' U R U2 r'", # Small Lightning Bolt
        "l' U' L U' L' U2 l", # Small Lightning Bolt
        "R U R' U' R' F R2 U R' U' F'", # Fish Shape
        "R U R' U R' F R F' R U2 R'", # Fish Shape
        "r U R' U R' F R F' R U2 r'", # Small Lightning Bolt
        "M' R' U' R U' R' U2 R U' R r'", # Small Lightning Bolt
        "F U R U' R2 F' R U R U' R'", # Knight Move Shape
        "R' F R U R' F' R F U' F'", # Knight Move Shape
        "l' U' l L' U' L U l' U l", # Knight Move Shape
        "r U r' R U R' U' r U' r'", # Knight Move Shape
        "F R' F' R2 r' U R U' R' U' M'", # Dot
        "r U R' U R U2 r2 U' R U' R' U2 r", # Dot
        "r' R U R U R' U' M' R' F R F'", # Dot
        "r U R' U' M2 U R U' R' U' M'", # Dot
        "R U2 R' U' R U R' U' R U' R'", # Cross
        "R U2 R2 U' R2 U' R2 U2 R", # Cross
        "R2 D' R U2 R' D R U2 R", # Cross
        "r U R' U' r' F R F'", # Cross
        "F' r U R' U' r' F R", # Cross
        "R U2 R' U' R U' R'", # Cross
        "R U R' U R U2 R'", # Cross
        "r U R' U' r' R U R U' R'", # Corners Oriented
        "R U R' U' R U' R' F' U' F R U R'", # Awkward Shape
        "F R' F R2 U' R' U' R U R' F2", # Awkward Shape
        "R' U' F U R U' R' F' R", # P Shape
        "L U F' U' L' U L F L'", # P Shape
        "R U R' U' R' F R F'", # T Shape
        "R U R2 U' R' F R U R U' F'", # C Shape
        "R U2 R2 F R F' R U2 R'", # Fish Shape
        "L' U' L U' L' U L U L F' L' F", # W Shape
        "F R' F' R U R U' R'", # Fish Shape
        "R U R' U R U' R' U' R' F R F'", # W Shape
        "L F' L' U' L U F U' L'", # Big Lightning Bolt
        "R' F R U R' U' F' U R", # Big Lightning Bolt
        "R U R' U R U2 R' F R U R' U' F'", # Awkward Shape
        "R' U' R U' R' U2 R F R U R' U' F'", # Awkward Shape
        "F' U' L' U L F", # P Shape
        "F U R U' R' F'", # P Shape
        "F R U R' U' F'", # T Shape
        "R' U' R' F R F' U R", # C Shape
        "R' U' R' F R F' R' F R F' U R", # Small L Shape
        "F R U R' U' R U R' U' F'", # Small L Shape
        "r U' r2 U r2 U r2 U' r", # Small L Shape
        "r' U r2 U' r2 U' r2 U r'", # Small L Shape
        "F U R U' R' U R U' R' F'", # I Shape
        "R U R' U R U' B U' B' R'", # I Shape
        "l' U2 L U L' U' L U L' U l", # Small L Shape
        "r U2 R' U' R U R' U' R U' r'", # Small L Shape
        "R' F R U R U' R2 F' R2 U' R' U R U R'", # I Shape
        "r' U' r U' R' U R U' R' U R r' U r", # I Shape
        "R U R' U' M' U R U' r'", # Corners Oriented
    ]

    # PLL
    Aa = "L2 B2 L' F' L B2 L' F L'" # Adjacent Corner Swap
    Ab = "L2 F2 L B L' F2 L B' L" # Adjacent Corner Swap
    F = "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R" # Adjacent Corner Swap
    Ga = "R2 U R' U R' U' R U' R2 U' D R' U R D'" # Adjacent Corner Swap
    Gb = "R' U' R U D' R2 U R' U R U' R U' R2 D" # Adjacent Corner Swap
    Gc = "R2 U' R U' R U R' U R2 U D' R U' R' D" # Adjacent Corner Swap
    Gd = "R U R' U' D R2 U' R U' R' U R' U R2 D'" # Adjacent Corner Swap
    Ja = "x R2 F R F' R U2 r' U r U2" # Adjacent Corner Swap
    Jb = "R U R' F' R U R' U' R' F R2 U' R'" # Adjacent Corner Swap
    Ra = "R U' R' U' R U R D R' U' R D' R' U2 R'" # Adjacent Corner Swap
    Rb = "R2 F R U R U' R' F' R U2 R' U2 R" # Adjacent Corner Swap
    T = "R U R' U' R' F R2 U' R' U' R U R' F'" # Adjacent Corner Swap
    E = "x' L' U L D' L' U' L D L' U' L D' L' U L D" # Diagonal Corner Swap
    Na = "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'" # Diagonal Corner Swap
    Nb = "R' U R U' R' F' U' F R U R' F R' F' R U' R" # Diagonal Corner Swap
    V = "R' U R' U' y R' F' R2 U' R' U R' F R F" # Diagonal Corner Swap
    Y = "F R U' R' U' R U R' F' R U R' U' R' F R F'" # Diagonal Corner Swap
    H = "M2 U M2 U2 M2 U M2" # Edges Only
    Ua = "M2 U M U2 M' U M2" # Edges Only
    Ub = "M2 U' M U2 M' U' M2" # Edges Only
    Z = "M' U M2 U M2 U M' U2 M2" # Edges Only


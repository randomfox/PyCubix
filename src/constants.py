from enums import *

class Constants:
    known_moves = [
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

    move_to_face_rotation_map = {
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

    face_rotation_to_move_map = {
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

    cw_face_rotations = [
        FaceRotation.FRONT_CW,
        FaceRotation.BACK_CW,
        FaceRotation.LEFT_CW,
        FaceRotation.RIGHT_CW,
        FaceRotation.UP_CW,
        FaceRotation.DOWN_CW
    ]

    ccw_face_rotations = [
        FaceRotation.FRONT_CCW,
        FaceRotation.BACK_CCW,
        FaceRotation.LEFT_CCW,
        FaceRotation.RIGHT_CCW,
        FaceRotation.UP_CCW,
        FaceRotation.DOWN_CCW
    ]

    sexy_move_trigger = "R U R' U'"
    sledgehammer_trigger = "R' F R F'"

    # pattern nicked from https://ruwix.com/the-rubiks-cube/rubiks-cube-patterns-algorithms/
    checkerboard_pattern = "U2 D2 F2 B2 L2 R2"
    cubeincube_pattern = "F L F U' R U F2 L2 U' L' B D' B' L2 U"
    four_crosses_pattern = "U2 R2 L2 F2 B2 D2 L2 R2 F2 B2"
    four_spots_pattern = "F2 B2 U D' R2 L2 U D'"
    plusminus_pattern = "U2 R2 L2 U2 R2 L2"
    six_spots_pattern = "U D' R L' F B' U D'"
    superflip_pattern = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    tetris_pattern = "L R F B U' D' L' R'"
    verticalstripes_pattern = "F U F R L2 B D' R D2 L D' B R2 L F U F"

    @staticmethod
    def is_known_move(str):
        for move in Constants.known_move:
            if move == str:
                return True
        return False

    @staticmethod
    def get_face_rotation_by_move(str):
        return Constants.move_to_face_rotation_map.get(str)

    @staticmethod
    def get_move_by_face_rotation(face):
        return Constants.face_rotation_to_move_map.get(face)

    @staticmethod
    def is_cw_face_rotation(face):
        for cwf in Constants.cw_face_rotations:
            if face == cwf:
                return True
        return False

    @staticmethod
    def is_ccw_face_rotation(face):
        for ccwf in Constants.ccw_face_rotations:
            if face == ccwf:
                return True
        return False

from enums import *

class Constants:
    known_str_face_rotations = [
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

    str_to_face_rotation_map = {
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

    face_rotation_to_str_map = {
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

    sexy_move = [
        FaceRotation.RIGHT_CW,
        FaceRotation.UP_CW,
        FaceRotation.RIGHT_CCW,
        FaceRotation.UP_CCW
    ]

    sledgehammer_move = [
        FaceRotation.RIGHT_CCW,
        FaceRotation.FRONT_CW,
        FaceRotation.RIGHT_CW,
        FaceRotation.FRONT_CCW
    ]

    @staticmethod
    def is_known_face_rotation(str):
        for face in Constants.known_str_face_rotations:
            if face == str:
                return True
        return False

    @staticmethod
    def get_face_rotation_by_str(str):
        return Constants.str_to_face_rotation_map[str]

    @staticmethod
    def get_str_by_face_rotation(face):
        return Constants.face_rotation_to_str_map[face]

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

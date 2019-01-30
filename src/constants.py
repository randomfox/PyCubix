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

    @staticmethod
    def is_known_face_rotation(str):
        for face_rot in known_str_face_rotations:
            if face_rot == str:
                return True
        return False
    @staticmethod

    def get_face_rotation_by_str(str):
        return str_to_face_rotation_map[str]

    def get_str_by_face_rotation(face_rot):
        return face_rotation_to_str_map[face_rot]

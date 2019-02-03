from constants import Constants
import random

class LittleHelpers:
    @staticmethod
    def is_known_notation(str):
        for move in Constants.KNOWN_NOTATIONS:
            if move == str:
                return True
        return False

    @staticmethod
    def get_face_rotation_by_notation(str):
        return Constants.NOTATION_TO_FACE_ROTATION_MAP.get(str)

    @staticmethod
    def get_notation_by_face_rotation(face):
        return Constants.FACE_ROTATION_TO_NOTATION_MAP.get(face)

    @staticmethod
    def is_cw_face_rotation(face):
        for cw in Constants.CW_FACE_ROTATIONS:
            if face == cw:
                return True
        return False

    @staticmethod
    def is_ccw_face_rotation(face):
        for ccw in Constants.CCW_FACE_ROTATION:
            if face == ccw:
                return True
        return False

    @staticmethod
    def translate_moves_to_face_rotations(moves):
        face_rotations = []
        for move in moves:
            face_rotation = LittleHelpers.get_face_rotation_by_notation(move)
            if face_rotation != None:
                face_rotations.append(face_rotation)
        return face_rotations

    @staticmethod
    # expand notations like "R2" to "R R"
    # not supported are notations like "R2'"
    def expand_notations(str):
        expanded_notations = []
        for move in str:
            length = len(move)
            if length == 2:
                if move[1] == '2':
                    expanded_notations.append(move[0])
                    expanded_notations.append(move[0])
                    continue
            expanded_notations.append(move)
        return expanded_notations

    # string format: "FACE1:COLOR1, FACE2:COLOR2, ...]
    # e.g. "FRONT:BLUE,BACK:GREEN,UP:WHITE, ..."
    @staticmethod
    def translate_cube_color_orienation(str):
        color_orientation = {}
        arr = str.split(",")
        if len(arr) != 6:
            return {}
        for face_to_color in arr:
            face_and_color = face_to_color.split(":")
            if len(face_and_color) != 2:
                return {}
            face_str = face_and_color[0].strip()
            color_str = face_and_color[1].strip()
            face = Constants.STR_TO_FACE_MAP.get(face_str)
            color = Constants.STR_TO_COLOR_MAP.get(color_str)
            if face == None or color == None:
                return {}
            color_orientation[face] = color
        return color_orientation

    @staticmethod
    def get_color_value_by_color(color):
        return Constants.COLOR_TO_COLOR_VALUE_MAP.get(color)

    @staticmethod
    def get_patterns():
        return [
            Constants.CHECKERBOARD_PATTERN,
            Constants.CUBE_IN_CUBE_PATTERN,
            Constants.FOUR_CROSSES_PATTERN,
            Constants.FOUR_SPOTS_PATTERN,
            Constants.PLUS_MINUS_PATTERN,
            Constants.SIX_SPOTS_PATTERN,
            Constants.SUPERFLIP_PATTERN,
            Constants.TETRIS_PATTERN,
            Constants.VERTICAL_STRIPES_PATTERN
        ]

    @staticmethod
    def get_random_pattern():
        return random.choice(LittleHelpers.get_patterns())


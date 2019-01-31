from constants import Constants
import random

class CubeHelpers:
    @staticmethod
    def translate_moves_to_face_rotations(moves):
        face_rotations = []
        for move in moves:
            face_rotation = Constants.get_face_rotation_by_move(move)
            if face_rotation != None:
                face_rotations.append(face_rotation)
        return face_rotations

    @staticmethod
    # expand moves like "R2" to "R R"
    # not supported are notations like "R2'"
    def expand_moves(moves):
        expanded_moves = []
        for move in moves:
            length = len(move)
            if length == 2:
                if move[1] == '2':
                    expanded_moves.append(move[0])
                    expanded_moves.append(move[0])
                    continue
            expanded_moves.append(move)
        return expanded_moves

    @staticmethod
    def get_random_pattern():
        patterns = [
            Constants.checkerboard_pattern,
            Constants.cubeincube_pattern,
            Constants.four_crosses_pattern,
            Constants.four_spots_pattern,
            Constants.plusminus_pattern,
            Constants.six_spots_pattern,
            Constants.superflip_pattern,
            Constants.tetris_pattern,
            Constants.verticalstripes_pattern
            ]
        return random.choice(patterns)


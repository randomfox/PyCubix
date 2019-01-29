""" PyCube
Author: Michael King

Based and modified from original version found at:
http://stackoverflow.com/questions/30745703/rotating-a-cube-using-quaternions-in-pyopengl
"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from quat import *
from geometry import *
from math import *
from collections import deque
from tween import Tween

from enums import *

class Cube:
    def __init__(self, initial_padding, face_turn_tween_time, draw_sphere, draw_lines):
        self.moves = deque()
        # self.pad_toggle = False

        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)
        self.scale = 1

        self.padding = initial_padding
        self.face_turn_tween_time = face_turn_tween_time
        self.draw_lines = draw_lines
        self.draw_sphere = draw_sphere

        self.sphere_radius = 3
        self.sphere_slices = 16
        self.sphere_stacks = 16

        self.state = State.IDLE

        self.tween = Tween()
        self.current_move = None

        add_padding(0.3)

    def update(self, elapsed_time):
        rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.rot_x))
        rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.rot_y))

        self.accum = q_mult(self.accum, rot_x)
        self.accum = q_mult(self.accum, rot_y)

        self.update_moves()
        self.update_tween(elapsed_time)
        self.update_face_turn(elapsed_time)

    def render(self):
        glPushMatrix()
        glLoadMatrixf(q_to_mat4(self.accum))
        glScalef(self.scale, self.scale, self.scale)

        if self.draw_sphere:
            glutSolidSphere(self.sphere_radius, self.sphere_slices, self.sphere_stacks)

        self.render_stickers()

        if self.draw_lines:
            self.render_lines()
        glPopMatrix()

    # def add_padding(self, value):
    #     new_padding = max(self.min_padding, min(self.padding + value, self.max_padding))
    #     delta = new_padding - self.padding
    #     # print("padding", self.padding, "new", new_padding, "delta", delta)
    #     add_padding(delta)
    #     self.padding = new_padding

    def add_rotate_x(self, value):
        self.rot_x += value

    def add_rotate_y(self, value):
        self.rot_y += value

    def add_scale(self, value):
        self.scale = max(self.scale + value, 0.1)

    def reset(self):
        self.reset_rotation()
        self.reset_scale()

    def reset_rotation(self):
        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)

    def reset_scale(self):
        self.scale = 1

    def stop_rotation(self):
        self.rot_x = 0
        self.rot_y = 0

    def add_move(self, face):
        self.moves.append(face)

    def update_moves(self):
        if self.state == State.TWEENING:
            return
        if len(self.moves) == 0:
            return

        self.current_move = self.moves.popleft()
        self.state = State.TWEENING

        self.tween.tween(0.0, pi/2, self.face_turn_tween_time)
        # print("current_move", self.current_move)

    def update_tween(self, elapsed_time):
        if self.state != State.TWEENING:
            return
        if not self.tween.is_done():
            self.tween.update(elapsed_time)
            # print(self.tween.current, self.tween.elapsed)
        else:
            self.state = State.IDLE
            self.current_move = None

    def update_face_turn(self, elapsed_time):
        delta = self.tween.get_delta()
        # Front face
        if self.current_move == Face.FRONT_CW:
            self.turn_front_face(-delta)
        elif self.current_move == Face.FRONT_CCW:
            self.turn_front_face(delta)
        # Back face
        elif self.current_move == Face.BACK_CW:
            self.turn_back_face(delta)
        elif self.current_move == Face.BACK_CCW:
            self.turn_back_face(-delta)
        # Left face
        elif self.current_move == Face.LEFT_CW:
            self.turn_left_face(delta)
        elif self.current_move == Face.LEFT_CCW:
            self.turn_left_face(-delta)
        # Right face
        elif self.current_move == Face.RIGHT_CW:
            self.turn_right_face(-delta)
        elif self.current_move == Face.RIGHT_CCW:
            self.turn_right_face(delta)
        # Up face
        elif self.current_move == Face.UP_CW:
            self.turn_up_face(-delta)
        elif self.current_move == Face.UP_CCW:
            self.turn_up_face(delta)
        # Down face
        elif self.current_move == Face.DOWN_CW:
            self.turn_down_face(delta)
        elif self.current_move == Face.DOWN_CCW:
            self.turn_down_face(-delta)

    def turn_front_face(self, theta):
        for i in range(8):
            center_pieces[0][i] = z_rot(center_pieces[0][i], theta)
        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[2] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theta)

    def turn_back_face(self, theta):
        for i in range(8):
            center_pieces[2][i] = z_rot(center_pieces[2][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[2] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theta)

    def turn_left_face(self, theta):
        for i in range(8):
            center_pieces[1][i] = x_rot(center_pieces[1][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    def turn_right_face(self, theta):
        for i in range(8):
            center_pieces[3][i] = x_rot(center_pieces[3][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    def turn_up_face(self, theta):
        for i in range(8):
            center_pieces[4][i] = y_rot(center_pieces[4][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)

    def turn_down_face(self, theta):
        for i in range(8):
            center_pieces[5][i] = y_rot(center_pieces[5][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)

    def render_lines(self):
        glLineWidth(GLfloat(6.0))
        glBegin(GL_LINES)
        glColor3fv((0.0, 0.0, 0.0))

        for axis in edge_pieces:
            for piece in axis:
                for edge in cube_edges:
                    for vertex in edge:
                        glVertex3fv(piece[vertex])
        for piece in center_pieces:
            for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(piece[vertex])
        for piece in corner_pieces:
            for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(piece[vertex])
        glEnd()

    def render_stickers(self):
        glBegin(GL_QUADS)
        i = 0
        for color, surface in zip(cube_colors, cube_surfaces):
            glColor3fv(color)
            for vertex in surface:
                glVertex3fv(center_pieces[i][vertex])
            j = 0
            for piece in center_pieces:
                glColor3fv((0, 0, 0))
                for vertex in surface:
                    glVertex3fv(center_pieces[j][vertex])
                j += 1
            i += 1

        for color, surface, face in zip(cube_colors, cube_surfaces, edges):
            glColor3fv(color)
            for piece in face:
                for vertex in surface:
                    glVertex3fv(edge_pieces[piece[0]][piece[1]][vertex])

        # Black inner sides of edge pieces
        edge_black_pat = [
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5]
            # [4, 5],
            # [0, 2]
        ]

        glColor3fv((0, 0, 0))

        for i in range(len(edge_black_pat)):
            for face in edge_black_pat[i]:
                for piece in edge_pieces[i]:
                    for vertex in cube_surfaces[face]:
                        glVertex3fv(piece[vertex])

        corner_color_pat = [
            [0, 1, 5],  # 0
            [0, 1, 4],  # 1
            [0, 3, 4],  # 2
            [0, 3, 5],  # 3
            [2, 1, 5],  # 4
            [2, 1, 4],  # 5
            [2, 3, 4],  # 6
            [2, 3, 5],  # 7
        ]

        corner_black_pat = [
            [2, 3, 4],  # 0
            [2, 3, 5],  # 1
            [2, 1, 5],  # 2
            [2, 1, 4],  # 3
            [0, 3, 4],  # 4
            [0, 3, 5],  # 5
            [0, 1, 5],  # 6
            [0, 1, 4],  # 7
        ]

        for i in range(len(corner_color_pat)):
            for face in corner_color_pat[i]:
                glColor3fv(cube_colors[face])
                for vertex in cube_surfaces[face]:
                    glVertex3fv(corner_pieces[i][vertex])
        glColor3fv((0, 0, 0))
        for i in range(len(corner_black_pat)):
            for face in corner_black_pat[i]:
                for vertex in cube_surfaces[face]:
                    glVertex3fv(corner_pieces[i][vertex])
        glEnd()

    def render_axis(self):
        glLineWidth(GLfloat(1.0))
        glBegin(GL_LINES)

        for color, axis in zip(axis_colors, axes):
            glColor3fv(color)
            for point in axis:
                glVertex3fv(axis_verts[point])
        glEnd()

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
    def __init__(self):
        self.moves = deque()
        self.pad_toggle = False

        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)
        self.zoom = 1

        self.state = State.IDLE

        self.tween = Tween()
        self.current_move = None

        padding(0.3)

    def update(self, elapsed_time):
        rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.rot_x * elapsed_time))
        rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.rot_y * elapsed_time))

        self.accum = q_mult(self.accum, rot_x)
        self.accum = q_mult(self.accum, rot_y)

        self.update_moves()
        self.update_tween(elapsed_time)
        self.update_face_turn(elapsed_time)

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(q_to_mat4(self.accum))
        glScalef(self.zoom, self.zoom, self.zoom)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glutSolidSphere(3.0, 50, 50);
        self.draw_stickers()
        self.draw_lines()

    def rotate_x(self, speed):
        self.rot_x = speed

    def rotate_y(self, speed):
        self.rot_y = speed

    def reset_rotation(self):
        self.rot_x = 0
        self.rot_y = 0
        self.accum = (1, 0, 0, 0)
        self.zoom = 1

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

        self.tween.tween(0.0, pi/2, 0.5)
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

    # def run(self):
    #     while True:
    #         theta_inc = 7
    #         theta = pi / 2 / theta_inc

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 print()
    #                 pygame.quit()
    #                 quit()
    #                 # elif event.type == VIDEORESIZE:
    #                 # self.CreateWindow(event.w, event.h)
    #                 # update()

    #             if event.type == pygame.KEYDOWN:
    #                 # Rotating about the x axis
    #                 if event.key == pygame.K_UP:  # or event.key == pygame.K_w:
    #                     self.inc_x = pi / 100
    #                 if event.key == pygame.K_DOWN:  # or event.key == pygame.K_s:
    #                     self.inc_x = -pi / 100

    #                 # Rotating about the y axis
    #                 if event.key == pygame.K_LEFT:  # or event.key == pygame.K_a:
    #                     self.inc_y = pi / 100
    #                 if event.key == pygame.K_RIGHT:  # or event.key == pygame.K_d:
    #                     self.inc_y = -pi / 100

    #                 if event.key == pygame.K_f:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves += 'F'
    #                         sys.stdout.write("F\'")
    #                         theta *= 1
    #                     else:
    #                         self.moves += 'f'
    #                         sys.stdout.write("F")
    #                         theta *= -1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[0][i] = z_rot(center_pieces[0][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[2] < 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = z_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[2] < 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = z_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_l:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves += 'L'
    #                         sys.stdout.write("L\'")
    #                         theta *= -1
    #                     else:
    #                         self.moves += 'l'
    #                         sys.stdout.write("L")
    #                         theta *= 1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[1][i] = x_rot(center_pieces[1][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[0] > 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = x_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[0] > 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = x_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_b:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves += 'B'
    #                         sys.stdout.write("B\'")
    #                         theta *= -1
    #                     else:
    #                         self.moves += 'b'
    #                         sys.stdout.write("B")
    #                         theta *= 1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[2][i] = z_rot(center_pieces[2][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[2] > 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = z_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[2] > 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = z_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_r:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves += 'R'
    #                         sys.stdout.write("R\'")
    #                         theta *= 1
    #                     else:
    #                         self.moves += 'r'
    #                         sys.stdout.write("R")
    #                         theta *= -1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[3][i] = x_rot(center_pieces[3][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[0] < 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = x_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[0] < 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = x_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_u:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves += 'U'
    #                         sys.stdout.write("U\'")
    #                         theta *= 1
    #                     else:
    #                         self.moves += 'u'
    #                         sys.stdout.write("U")
    #                         theta *= -1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[4][i] = y_rot(center_pieces[4][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[1] < 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = y_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[1] < 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = y_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_d:
    #                     if pygame.key.get_mods() & KMOD_SHIFT:
    #                         self.moves +='D'
    #                         sys.stdout.write("D\'")
    #                         theta *= -1
    #                     else:
    #                         self.moves += 'd'
    #                         sys.stdout.write("D")
    #                         theta *= 1
    #                     for x in range(theta_inc):
    #                         for i in range(8):
    #                             center_pieces[5][i] = y_rot(center_pieces[5][i], theta)

    #                         for axis in edge_pieces:
    #                             for piece in axis:
    #                                 flag = True
    #                                 for vertex in piece:
    #                                     if vertex[1] > 0:
    #                                         flag = False
    #                                         break
    #                                 if flag:
    #                                     for i in range(8):
    #                                         piece[i] = y_rot(piece[i], theta)
    #                         for piece in corner_pieces:
    #                             flag = True
    #                             for vertex in piece:
    #                                 if vertex[1] > 0:
    #                                     flag = False
    #                                     break
    #                             if flag:
    #                                 for i in range(8):
    #                                     piece[i] = y_rot(piece[i], theta)

    #                         self.update()

    #                 if event.key == pygame.K_e:
    #                     self.pad_toggle = not self.pad_toggle

    #                 # Reset to default view
    #                 if event.key == pygame.K_SPACE:
    #                     self.inc_x = 0
    #                     self.inc_y = 0
    #                     self.accum = (1, 0, 0, 0)
    #                     self.zoom = 1

    #                 if event.key == pygame.K_EQUALS:
    #                     p = multiprocessing.Process(target=keypress.wail, args=(self.moves,))
    #                     # thread.daemon = True
    #                     p.start()
    #                     p.join()
    #                     print()
    #                     print(self.moves)
    #                     self.moves = ''
    #                     print(self.moves)

    #                 if event.key == pygame.K_MINUS:
    #                     mvs = 'fFbBlLrRuUdD'
    #                     scrambled = ''.join(random.choice(mvs) for _ in range(20))
    #                     p = multiprocessing.Process(target=self.scramble, args=(scrambled,))
    #                     # p.daemon = True
    #                     p.start()
    #                     p.join()
    #                     # self.scramble()

    #             if event.type == pygame.KEYUP:
    #                 # Stoping rotation
    #                 if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
    #                                 event.key == pygame.K_w or event.key == pygame.K_s:
    #                     self.inc_x = 0.0
    #                 if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
    #                                 event.key == pygame.K_a or event.key == pygame.K_d or \
    #                                 event.key == pygame.K_l or event.key == pygame.K_f:
    #                     self.inc_y = 0.0

    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 # Increase scale (zoom) value
    #                 if event.button == 4 and self.zoom < 1.6 and not (pygame.key.get_mods() & KMOD_SHIFT):
    #                     self.zoom += 0.05
    #                     # print('scroll up', zoom)
    #                 if event.button == 5 and self.zoom > 0.3 and not (pygame.key.get_mods() & KMOD_SHIFT):
    #                     self.zoom -= 0.05
    #                     # print('scroll down', zoom)

    #                     # change padding with [shift] mousewheel
    #                     # if event.button == 5 and abs(center_pieces[0][0][2])>3.2 and pygame.key.get_mods() & KMOD_SHIFT:
    #                     #     padding(-0.2)
    #                     # if event.button == 4 and abs(center_pieces[0][0][2])<=6 and pygame.key.get_mods() & KMOD_SHIFT:
    #                     #      padding(0.2)

    #         # Get relative movement of mouse coordinates and update x and y incs
    #         if pygame.mouse.get_pressed()[0] == 1:
    #             (tmp_x, tmp_y) = pygame.mouse.get_rel()
    #             # print(tmp_x, tmp_y)
    #             self.inc_x = -tmp_y * pi / 450
    #             self.inc_y = -tmp_x * pi / 450

    #         if self.pad_toggle and abs(center_pieces[0][0][2]) <= 6:
    #             padding(0.3)
    #         elif abs(center_pieces[0][0][2]) > 3.3 and not self.pad_toggle:
    #             padding(-0.3)

    #         self.update()
    #         sys.stdout.flush()
    #         # time.sleep(5000)

    # def scramble(self, scrambled):

    #     keypress.wail(scrambled)

    def draw_lines(self):
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

    def draw_stickers(self):
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

    def draw_axis(self):
        glLineWidth(GLfloat(1.0))
        glBegin(GL_LINES)

        for color, axis in zip(axis_colors, axes):
            glColor3fv(color)
            for point in axis:
                glVertex3fv(axis_verts[point])
        glEnd()

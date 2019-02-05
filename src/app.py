import time
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

from constants import Constants
from cube import Cube
from delta_time import DeltaTime
from enums import *
from fps import Fps
from helpers import LittleHelpers

class App:
    KEY_BACKSPACE = 8
    KEY_RETURN = 13
    KEY_ESCAPE = 27

    def __init__(self, settings, subscriber):
        self.settings = settings
        self.subscriber = subscriber

        self.delta_time = DeltaTime()
        self.fps = Fps(self.settings.fps_update_interval)
        self.show_fps = True

        self.command_delimiter = ';'

        self.init_opengl()
        self.init_cube()

        if "--glinfo" in sys.argv:
            self.show_gl_info()

    def init_opengl(self):
        glutInit()
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.settings.window_width, self.settings.window_height)
        glutCreateWindow(self.settings.window_caption)

        glutReshapeFunc(self.on_reshape_window)
        glutKeyboardFunc(self.on_keyboard_input)
        glutSpecialFunc(self.on_special_input)
        glutVisibilityFunc(self.on_visibility_change)
        glutIdleFunc(self.on_update)
        glutDisplayFunc(self.on_display)
        glutCloseFunc(self.on_close_window)

        clear_color = self.settings.window_background_color
        glClearColor(clear_color[0], clear_color[1], clear_color[2], 1)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)
        glDepthFunc(GL_LESS)

    def init_cube(self):
        # :TODO: un-uglify!
        padding = self.settings.cube_padding
        draw_cubies = self.settings.cube_draw_cubies
        draw_sphere = self.settings.cube_draw_sphere
        draw_lines = self.settings.cube_draw_lines
        line_width = self.settings.cube_line_width
        inner_color = self.settings.cube_inner_color
        sphere_color = self.settings.cube_sphere_color

        tween_time = self.settings.cube_face_rotation_tween_time
        ease_type = LittleHelpers.get_ease_type_by_str(self.settings.cube_face_rotation_ease_type)
        angular_drag = self.settings.cube_angular_drag

        self.cube = Cube(padding, draw_cubies, draw_sphere, draw_lines, line_width, inner_color, sphere_color, tween_time, ease_type, angular_drag)
        self.set_cube_color_orientation(self.settings.cube_color_orientation_str)

        # this is a hack, more or less, but it is how it is.
        try:
            front_color = self.settings.cube_face_colors['blue']
            back_color = self.settings.cube_face_colors['green']
            left_color = self.settings.cube_face_colors['orange']
            right_color = self.settings.cube_face_colors['red']
            up_color = self.settings.cube_face_colors['yellow']
            down_color = self.settings.cube_face_colors['white']
            self.cube.set_color_orientation(front_color, back_color, left_color, right_color, up_color, down_color)
        except:
            print('WTF. Check your colors.')

    def run(self):
        glutMainLoop()

    def show_gl_info(self):
        print("* GL_RENDERER   :", glGetString(GL_RENDERER))
        print("* GL_VERSION    : ", glGetString(GL_VERSION))
        print("* GL_VENDOR     : ", glGetString(GL_VENDOR))
        print("* GL_EXTENSIONS : ", glGetString(GL_EXTENSIONS))

    def prepare_exit(self):
        self.subscriber.stop()

    def on_close_window(self):
        self.prepare_exit()

    def on_reshape_window(self, w, h):
        if h == 0:
            h = 1
        ratio = 1.0 * w / h

        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, ratio, 0.1, 100)
        glTranslatef(0.0, 0.0, -17.5)
        glMatrixMode(GL_MODELVIEW)

    def on_visibility_change(self, visible):
        if visible == GLUT_VISIBLE:
            glutIdleFunc(self.on_update)
        else:
            glutIdleFunc(None)

    def on_keyboard_input(self, key, x, y):
        ch = key.decode("utf-8")

        # exit app on q or ESC:
        if ch == 'q' or ch == chr(self.KEY_ESCAPE):
            self.prepare_exit()
            sys.exit()
        # reset cube:
        elif ch == chr(self.KEY_BACKSPACE):
            self.cube.reset()
        # reset scale and rotation:
        elif ch == chr(self.KEY_RETURN):
            self.cube.reset_rotation()
            self.cube.reset_scale()
        # stop rotation:
        elif ch == ' ':
            self.cube.stop_rotation()
        # scramble with random pattern:
        elif ch == '1':
            pattern = LittleHelpers.get_random_pattern()
            self.cube.reset()
            self.scramble_cube(pattern)
        # apply random pattern:
        elif ch == '2':
            self.apply_random_pattern()
        # switch white and yellow:
        elif ch == '0':
            str = "front:blue, back:green, left:red, right:orange, up:white, down:yellow"
            self.set_cube_color_orientation(str)
        # debug test case:
        elif ch == 'x':
            self.test()

        scale = None
        if ch == '+':
            scale = 1
        elif ch == '-':
            scale = -1
        if scale != None:
            self.cube.inc_scale(scale * self.delta_time.elapsed())

        # translate move:
        move = None
        if ch == 'f':   move = "F"
        elif ch == 'F': move = "F'"
        elif ch == 'b': move = "B"
        elif ch == 'B': move = "B'"
        elif ch == 'u': move = "U"
        elif ch == 'U': move = "U'"
        elif ch == 'd': move = "D"
        elif ch == 'D': move = "D'"
        elif ch == 'l': move = "L"
        elif ch == 'L': move = "L'"
        elif ch == 'r': move = "R"
        elif ch == 'R': move = "R'"
        if move != None:
            self.add_moves([move])

    def on_special_input(self, key, x, y):
        value = pi / 32 * self.delta_time.elapsed()

        if key == GLUT_KEY_UP:
            self.cube.inc_rotate_x(value)
        if key == GLUT_KEY_DOWN:
            self.cube.inc_rotate_x(-value)
        if key == GLUT_KEY_LEFT:
            self.cube.inc_rotate_y(value)
        if key == GLUT_KEY_RIGHT:
            self.cube.inc_rotate_y(-value)

    def on_update(self):
        self.delta_time.update()
        self.cube.update(self.delta_time.elapsed())
        self.check_message_queue()
        glutPostRedisplay()

    def on_display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube.render()
        glutSwapBuffers()

        if self.show_fps:
            self.fps.update()

    def add_moves(self, moves):
        print('add_moves', moves)
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        if face_rotations:
            self.append_face_rotations(face_rotations)

    def append_face_rotations(self, face_rotations):
        for face_rotation in face_rotations:
            self.cube.append_face_rotation(face_rotation)

    # moves: array
    def scramble_cube(self, moves):
        print('scramble_cube', moves)
        moves = LittleHelpers.expand_notations(moves.split(' '))
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        self.cube.scramble(face_rotations)

    def set_cube_color_orientation(self, str):
        map = LittleHelpers.translate_cube_color_orientation(str.upper())
        if len(map) != 6:
            return
        print('set_cube_color_orientation', str)
        front_color = LittleHelpers.get_color_value_by_color(map.get(Face.FRONT))
        back_color = LittleHelpers.get_color_value_by_color(map.get(Face.BACK))
        left_color = LittleHelpers.get_color_value_by_color(map.get(Face.LEFT))
        right_color = LittleHelpers.get_color_value_by_color(map.get(Face.RIGHT))
        up_color = LittleHelpers.get_color_value_by_color(map.get(Face.UP))
        down_color = LittleHelpers.get_color_value_by_color(map.get(Face.DOWN))
        self.cube.set_color_orientation(front_color, back_color, left_color, right_color, up_color, down_color)

    def apply_random_pattern(self):
        pattern = LittleHelpers.get_random_pattern()
        print('apply_random_pattern', pattern)
        moves = LittleHelpers.expand_notations(pattern.split(' '))
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        self.append_face_rotations(face_rotations)

    def check_message_queue(self):
        if self.subscriber.has_pending_messages():
            message = self.subscriber.get_message()
            if message == None:
                return
            commands = message.strip().split(self.command_delimiter)
            for command in commands:
                self.handle_command(command)

    # :TODO: clean up this mess
    def handle_command(self, command):
        # print('Message handler |{}|'.format(command))
        if not command:
            return

        parts = command.split('=')

        num_parts = len(parts)
        if num_parts == 0:
            return

        for index, part in enumerate(parts):
            parts[index] = part.strip()

        cmd = parts[0]

        if cmd == 'quit' or cmd == 'exit':
            self.prepare_exit()
            sys.exit()

        elif cmd == 'reset_cube':
            self.cube.reset()

        elif cmd == 'reset_cube_rotation':
            self.cube.reset_rotation()

        elif cmd == 'reset_cube_scale':
            self.cube.reset_scale()

        elif cmd == 'stop_cube_rotation':
            self.cube.stop_rotation()

        elif cmd == 'apply_random_pattern':
            self.apply_random_pattern()

        elif cmd == 'add_rotation_x':
            if num_parts == 2:
                value = LittleHelpers.convert_str_to_float(parts[1])
                if value:
                    self.cube.inc_rotate_x(value * self.delta_time.elapsed())

        elif cmd == 'add_rotation_y':
            if num_parts == 2:
                value = LittleHelpers.convert_str_to_float(parts[1])
                if value:
                    self.cube.inc_rotate_y(value * self.delta_time.elapsed())

        elif cmd == 'rotate_face':
            moves = LittleHelpers.expand_notations(parts[1].upper().split(' '))
            self.add_moves(moves)

        elif cmd == 'scramble':
            moves = parts[1].upper()
            self.scramble_cube(moves)

        elif cmd == 'set_color_orientation':
            self.set_cube_color_orientation(parts[1])

        elif cmd == 'set_padding':
            value = LittleHelpers.convert_str_to_float(parts[1])
            if value:
                print('setting padding', value)
                self.cube.geometry.set_padding(value)

        else:
            print('Unknown command:', cmd)

    def test(self):
        pass

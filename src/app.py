import time
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

from constants import *
from cube import Cube
from delta_time import DeltaTime
from enums import *
from fps import Fps
from helpers import LittleHelpers
from mathf import Mathf
from mousedrag import MouseDrag

class App:
    KEY_BACKSPACE = 8
    KEY_RETURN = 13
    KEY_ESCAPE = 27

    def __init__(self, settings, subscriber, glinfo):
        self.settings = settings
        self.subscriber = subscriber

        self.delta_time = DeltaTime()
        self.fps = Fps(self.settings.fps_update_interval)
        self.mouse_drag = MouseDrag()

        self.command_delimiter = ';'

        self.init_opengl()
        self.init_cube()

        if glinfo:
            self.show_gl_info()

    def init_opengl(self):
        glutInit()
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.settings.window_width, self.settings.window_height)
        glutCreateWindow(self.settings.window_caption)

        glutReshapeFunc(self.on_reshape_window)
        glutKeyboardFunc(self.on_keyboard_input)
        glutMouseFunc(self.on_mouse_input)
        glutMotionFunc(self.on_mouse_move)
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
        face_rotation_ease_type = LittleHelpers.get_ease_type_by_str(self.settings.cube_face_rotation_ease_type)
        self.cube = Cube(self.settings, face_rotation_ease_type)
        self.set_cube_color_orientation(self.settings.cube_color_mapping)

    def run(self):
        glutMainLoop()

    def show_gl_info(self):
        print("* GL_RENDERER   : ", glGetString(GL_RENDERER))
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
            self.reset_cube()
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
            self.reset_cube()
            self.scramble_cube(pattern)
        # apply random pattern:
        elif ch == '2':
            self.apply_random_pattern()
        # switch white and yellow:
        elif ch == '0':
            str = "front:blue, back:green, left:red, right:orange, up:white, down:yellow"
            color_mapping = LittleHelpers.make_color_mapping_from_string(str)
            self.set_cube_color_orientation(color_mapping)
        # debug test case:
        elif ch == 'x':
            self.test()

        # scale cube:
        scale = None
        scale_value = 0.1
        if ch == '+': scale = scale_value
        elif ch == '-': scale = -scale_value
        if scale != None:
            self.cube.add_scale(scale * self.delta_time.elapsed())

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

    def on_mouse_input(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_drag.begin(x, y)
                self.cube.stop_rotation()
            if state == GLUT_UP:
                self.mouse_drag.end(x, y)

    def on_mouse_move(self, x, y):
        if self.mouse_drag.is_dragging:
            sensitivity = Mathf.clamp(self.settings.mouse_sensitivity, 0.1, 10)
            val = pi / 500 * sensitivity
            self.mouse_drag.update(x, y)
            dx, dy = self.mouse_drag.get_delta()
            if dx != 0:
                self.cube.add_rotate_x(-dy * val * self.delta_time.elapsed())
            if dy != 0:
                self.cube.add_rotate_y(-dx * val * self.delta_time.elapsed())

    def on_special_input(self, key, x, y):
        value = pi / 32 * self.delta_time.elapsed()

        if key == GLUT_KEY_UP:
            self.cube.add_rotate_x(value)
        if key == GLUT_KEY_DOWN:
            self.cube.add_rotate_x(-value)
        if key == GLUT_KEY_LEFT:
            self.cube.add_rotate_y(value)
        if key == GLUT_KEY_RIGHT:
            self.cube.add_rotate_y(-value)

    def on_update(self):
        self.delta_time.update()
        self.cube.update(self.delta_time.elapsed())
        self.check_message_queue()
        glutPostRedisplay()

    def on_display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube.render()
        glutSwapBuffers()

        if self.settings.fps_show:
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

    def set_cube_color_orientation(self, color_mapping):
        front_color = Constants.FALLBACK_COLOR
        back_color = Constants.FALLBACK_COLOR
        left_color = Constants.FALLBACK_COLOR
        right_color = Constants.FALLBACK_COLOR
        up_color = Constants.FALLBACK_COLOR
        down_color = Constants.FALLBACK_COLOR

        colors = self.settings.cube_colors
        try:
            front_color = LittleHelpers.get_mapped_color(Face.FRONT, color_mapping, colors)
            back_color = LittleHelpers.get_mapped_color(Face.BACK, color_mapping, colors)
            left_color = LittleHelpers.get_mapped_color(Face.LEFT, color_mapping, colors)
            right_color = LittleHelpers.get_mapped_color(Face.RIGHT, color_mapping, colors)
            up_color = LittleHelpers.get_mapped_color(Face.UP, color_mapping, colors)
            down_color = LittleHelpers.get_mapped_color(Face.DOWN, color_mapping, colors)
        except:
            pass
        self.cube.set_color_orientation(front_color, back_color, left_color, right_color, up_color, down_color)

    def apply_random_pattern(self):
        pattern = LittleHelpers.get_random_pattern()
        print('apply_random_pattern', pattern)
        moves = LittleHelpers.expand_notations(pattern.split(' '))
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        self.append_face_rotations(face_rotations)

    def reset_cube(self):
        self.cube.reset()

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
            self.reset_cube()

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
                    self.cube.add_rotate_x(value * self.delta_time.elapsed())

        elif cmd == 'add_rotation_y':
            if num_parts == 2:
                value = LittleHelpers.convert_str_to_float(parts[1])
                if value:
                    self.cube.add_rotate_y(value * self.delta_time.elapsed())

        elif cmd == 'add_scale':
            if num_parts == 2:
                value = LittleHelpers.convert_str_to_float(parts[1])
                if value:
                    self.cube.add_scale(value * self.delta_time.elapsed())

        elif cmd == 'rotate_face':
            moves = LittleHelpers.expand_notations(parts[1].upper().split(' '))
            self.add_moves(moves)

        elif cmd == 'scramble':
            moves = parts[1].upper()
            self.scramble_cube(moves)

        elif cmd == 'set_color_orientation':
            color_mapping = LittleHelpers.make_color_mapping_from_string(parts[1])
            self.set_cube_color_orientation(color_mapping)

        elif cmd == 'set_padding':
            value = LittleHelpers.convert_str_to_float(parts[1])
            if value:
                self.cube.geometry.set_padding(value)

        else:
            print('Unknown command:', cmd)

    def test(self):
        pass

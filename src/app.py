import time
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from cube import Cube
from math import *
from delta_time import DeltaTime
from fps import Fps
from enums import *
from constants import Constants
from cube_helpers import CubeHelpers

class App:
    def __init__(self, settings):
        self.settings = settings
        self.delta_time = DeltaTime()
        print(self.settings)
        self.fps = Fps(self.settings.fps_update_interval)
        self.show_fps = True

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
        # glutCloseFunc(self.on_close_window)

        clear_color = self.settings.window_background_color
        glClearColor(clear_color[0], clear_color[1], clear_color[2], 1)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)
        glDepthFunc(GL_LESS)

    def init_cube(self):
        padding = self.settings.cube_padding
        tween_time = self.settings.cube_face_rotation_tween_time
        draw_stickers = self.settings.cube_draw_stickers
        draw_sphere = self.settings.cube_draw_sphere
        draw_lines = self.settings.cube_draw_lines
        line_width = self.settings.cube_line_width
        self.cube = Cube(padding, tween_time, draw_stickers, draw_sphere, draw_lines, line_width)

    def run(self):
        glutMainLoop()

    def show_gl_info(self):
        print("* GL_RENDERER   :", glGetString(GL_RENDERER))
        print("* GL_VERSION    : ", glGetString(GL_VERSION))
        print("* GL_VENDOR     : ", glGetString(GL_VENDOR))
        print("* GL_EXTENSIONS : ", glGetString(GL_EXTENSIONS))

    def exit_app(self):
        pass

    def on_close_window(self):
        pass

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
        if ch == 'q' or ch == chr(27):
            sys.exit()
            # self.exit_app()
        # reset cube:
        elif ch == chr(8):
            self.cube.reset()
        # reset scale and rotation:
        elif ch == chr(13):
            self.cube.reset_rotation()
            self.cube.reset_scale()
        # stop rotation:
        elif ch == ' ':
            self.cube.stop_rotation()
        # test scramble
        elif ch == '1':
            pattern = CubeHelpers.get_random_pattern()
            moves = CubeHelpers.expand_notations(pattern.split(' '))
            self.scramble_cube(moves)
        elif ch == '2':
            pattern = CubeHelpers.get_random_pattern()
            moves = CubeHelpers.expand_notations(pattern.split(' '))
            face_rotations = CubeHelpers.translate_moves_to_face_rotations(moves)
            self.append_face_rotations(face_rotations)
        elif ch == '0':
            str = "FRONT:BLUE, BACK:GREEN, LEFT:RED, RIGHT:ORANGE, UP:WHITE, DOWN:YELLOW"
            self.set_cube_color_orienation(str)

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
        # self.read_message_queue()
        glutPostRedisplay()

    def on_display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube.render()
        glutSwapBuffers()

        if self.show_fps:
            self.fps.update()

    def add_moves(self, moves):
        face_rotations = CubeHelpers.translate_moves_to_face_rotations(moves)
        self.append_face_rotations(face_rotations)

    def append_face_rotations(self, face_rotations):
        for face_rotation in face_rotations:
            self.cube.append_face_rotation(face_rotation)

    # moves: array
    def scramble_cube(self, moves):
        face_rotations = CubeHelpers.translate_moves_to_face_rotations(moves)
        self.cube.reset()
        self.cube.scramble(face_rotations)

    # e.g. "FRONT:BLUE, BACK:GREEN, LEFT:RED, RIGHT:ORANGE, UP:WHITE, DOWN:YELLOW"
    def set_cube_color_orienation(self, str):
        map = CubeHelpers.translate_cube_color_orienation(str)
        if len(map) != 6:
            return
        front_color = CubeHelpers.get_color_value_by_color(map.get(Face.FRONT))
        back_color = CubeHelpers.get_color_value_by_color(map.get(Face.BACK))
        left_color = CubeHelpers.get_color_value_by_color(map.get(Face.LEFT))
        right_color = CubeHelpers.get_color_value_by_color(map.get(Face.RIGHT))
        up_color = CubeHelpers.get_color_value_by_color(map.get(Face.UP))
        down_color = CubeHelpers.get_color_value_by_color(map.get(Face.DOWN))
        self.cube.set_color_orientation(front_color, back_color, left_color, right_color, up_color, down_color)

    def read_message_queue(self):
        pass
        # message = self.server_control.get_message()
        # if message != None:
        #     self.handle_message(message)

    def handle_message(self, message):
        pass
        # print('handling_message', message)

    def test(self):
        pass

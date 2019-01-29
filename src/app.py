from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from cube import Cube
from math import *
from deltatime import DeltaTime
from enums import Face

class App:
    def __init__(self):
        self.delta_time = DeltaTime()

        width = 600
        height = 600
        caption = "PyCubix"
        background_color = (60/255, 67/255, 78/255)
        self.init_opengl(caption, width, height, background_color)

        cube_padding = 0.5
        face_turn_tween_time = 0.5
        draw_sphere = True
        draw_lines = False
        self.init_cube(cube_padding, face_turn_tween_time, draw_sphere, draw_lines)

    def init_opengl(self, caption, width, height, background_color):
        glutInit()
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow(caption)

        glutReshapeFunc(self.on_reshape_window)
        glutKeyboardFunc(self.on_keyboard_input)
        glutSpecialFunc(self.on_special_input)
        glutVisibilityFunc(self.on_visibility_change)
        glutIdleFunc(self.on_update)
        glutDisplayFunc(self.on_display)

        if len(background_color) < 3:
            background_color = (1, 1, 1)
        glClearColor(background_color[0], background_color[1], background_color[2], 1)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)
        glDepthFunc(GL_LESS)

    def init_cube(self, cube_padding, face_turn_tween_time, draw_sphere, draw_lines):
        self.cube = Cube(cube_padding, face_turn_tween_time, draw_sphere, draw_lines)

    def run(self):
        glutMainLoop()

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

    def turn_cube_face(self, move):
        move_map = {
            "F": Face.FRONT_CW,
            "F'": Face.FRONT_CCW,
            "B": Face.BACK_CW,
            "B'": Face.BACK_CCW,
            "U": Face.UP_CW,
            "U'": Face.UP_CCW,
            "D": Face.DOWN_CW,
            "D'": Face.DOWN_CCW,
            "L": Face.LEFT_CW,
            "L'": Face.LEFT_CCW,
            "R": Face.RIGHT_CW,
            "R'": Face.RIGHT_CCW
        }
        face = move_map.get(move)
        self.cube.add_move(face)

    def on_keyboard_input(self, key, x, y):
        ch = key.decode("utf-8")

        # Exit app on q or ESC
        if ch == 'q' or ch == chr(27):
            sys.exit()
        elif ch == chr(13):
            self.cube.reset()
        elif ch == ' ':
            self.cube.stop_rotation()

        scale = None
        if ch == '+':
            scale = 1
        elif ch == '-':
            scale = -1
        if scale != None:
            self.cube.add_scale(scale * self.delta_time.elapsed())

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
            self.turn_cube_face(move)

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
        glutPostRedisplay()

    def on_display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube.render()
        glutSwapBuffers()

    # def _glut_mouse(self, button, state, x, y):
    #     self._glut_update_modifiers()

    #     btn = 'left'
    #     if button == GLUT_RIGHT_BUTTON:
    #         btn = 'right'

    #     if state == GLUT_DOWN:
    #         self.dispatch_event('on_mouse_down', x, y, btn, self.modifiers)
    #     else:
    #         self.dispatch_event('on_mouse_up', x, y, btn, self.modifiers)

    # def _glut_mouse_motion(self, x, y):
    #     self.dispatch_event('on_mouse_move', x, y, self.modifiers)

    # def _glut_update_modifiers(self):
    #     self._modifiers = []
    #     mods = glutGetModifiers()
    #     if mods & GLUT_ACTIVE_SHIFT:
    #         self._modifiers.append('shift')
    #     if mods & GLUT_ACTIVE_ALT:
    #         self._modifiers.append('alt')
    #     if mods & GLUT_ACTIVE_CTRL:
    #         self._modifiers.append('ctrl')

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from cube import Cube
from math import *
from deltatime import DeltaTime
from enums import Face

class App:
    def __init__(self):
        self.caption = "Pybix"
        self.width = 1024
        self.height = 768

        self.delta_time = DeltaTime()
        self.cube = Cube()
        self.init_opengl(self.caption, self.width, self.height)

    def init_opengl(self, caption, width, height):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow(caption)

        glClearColor(1, 1, 1, 1)
        # glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glutInit()

        glutReshapeFunc(self.on_reshape_window)
        glutKeyboardFunc(self.on_keyboard_input)
        glutSpecialFunc(self.on_special_input)
        glutIdleFunc(self.update);
        glutDisplayFunc(self.display)

        self.on_reshape_window(width, height)

    def run(self):
        glutMainLoop()

    def on_reshape_window(self, w, h):
        if h == 0:
            h = 1
        ratio = 1.0 * w / h

        self.width = w
        self.height = h

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(45, ratio, 0.1, 100)
        glTranslatef(0.0, 0.0, -17.5)
        glMatrixMode(GL_MODELVIEW);

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

        if ch == chr(13):
            self.cube.reset_rotation()
        if ch == ' ':
            self.cube.stop_rotation()

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
        # print("special", key, x, y)
        speed = pi / 8

        if key == GLUT_KEY_UP:
            self.cube.rotate_x(speed)
        if key == GLUT_KEY_DOWN:
            self.cube.rotate_x(-speed)
        if key == GLUT_KEY_LEFT:
            self.cube.rotate_y(speed)
        if key == GLUT_KEY_RIGHT:
            self.cube.rotate_y(-speed)

    def update(self):
        self.delta_time.update()
        self.cube.update(self.delta_time.elapsed())
        glutPostRedisplay()

    def display(self):
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

    # def _glut_keyboard(self, key, x, y):
    #     self.dispatch_event('on_keyboard', key, None, None)

    # def _glut_update_modifiers(self):
    #     self._modifiers = []
    #     mods = glutGetModifiers()
    #     if mods & GLUT_ACTIVE_SHIFT:
    #         self._modifiers.append('shift')
    #     if mods & GLUT_ACTIVE_ALT:
    #         self._modifiers.append('alt')
    #     if mods & GLUT_ACTIVE_CTRL:
    #         self._modifiers.append('ctrl')

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from cube import Cube
from math import *
from deltatime import DeltaTime
from fps import Fps
from enums import *
from constants import Constants

class App:
    def __init__(self):
        self.delta_time = DeltaTime()

        update_interval = 10.0
        self.fps = Fps(update_interval)
        self.show_fps = True

        width = 600
        height = 600
        caption = "PyCubix"
        background_color = (60/255, 67/255, 78/255)
        self.init_opengl(caption, width, height, background_color)

        if "--glinfo" in sys.argv:
            self.show_gl_info()

        self.padding = 0.3
        self.face_rotation_tween_time = 0.5
        self.draw_stickers = True
        self.draw_sphere = True
        self.draw_lines = False
        self.init_cube(self.padding, self.face_rotation_tween_time, self.draw_stickers, self.draw_sphere, self.draw_lines)

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

    def init_cube(self, padding, face_rotation_tween_time, draw_stickers, draw_sphere, draw_lines):
        self.cube = Cube(padding, face_rotation_tween_time, draw_stickers, draw_sphere, draw_lines)

    def run(self):
        glutMainLoop()

    def show_gl_info(self):
        print("* GL_RENDERER   :", glGetString(GL_RENDERER))
        print("* GL_VERSION    : ", glGetString(GL_VERSION))
        print("* GL_VENDOR     : ", glGetString(GL_VENDOR))
        print("* GL_EXTENSIONS : ", glGetString(GL_EXTENSIONS))

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

    def rotate_face(self, move):
        face = Constants.str_to_face_rotation_map.get(move)
        self.cube.add_move(face)

    def on_keyboard_input(self, key, x, y):
        ch = key.decode("utf-8")

        # Exit app on q or ESC
        if ch == 'q' or ch == chr(27):
            sys.exit()
        # reset cube
        elif ch == chr(8):
            self.init_cube(self.padding, self.face_rotation_tween_time, self.draw_stickers, self.draw_sphere, self.draw_lines)
        # reset scale and rotation
        elif ch == chr(13):
            self.cube.reset_rotation()
            self.cube.reset_scale()
        # stop rotation
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
            self.rotate_face(move)

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

        if self.show_fps:
            self.fps.update()

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

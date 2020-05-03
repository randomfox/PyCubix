import atexit
import time
import sys

# my stuff
import random


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
from mqttclient import *
from mousedrag import MouseDrag
from tween import *

class App:
    KEY_BACKSPACE = 8
    KEY_RETURN = 13
    KEY_ESCAPE = 27
    KEY_DELETE = 127

    def __init__(self, settings, color_manager, display_glinfo):
        self.settings = settings
        self.color_manager = color_manager
        self.client = None
        self.colors = None
        self.color_mapping = {}

        self.delta_time = DeltaTime()
        self.fps = Fps(self.settings.fps_update_interval)
        self.mouse_drag = MouseDrag()

        self.command_delimiter = ';'

        self.init_colors()
        self.init_opengl()

        self.textures = {}
        if self.settings.texture_mapping_enabled:
            self.create_textures(self.settings.image_resources)

        self.init_cube()
        self.init_command_handler_map()

        if self.settings.mqtt_client_start:
            self.init_mqtt_client()

        if display_glinfo:
            self.show_gl_info()

        atexit.register(self.on_exit)

        self.states = ['CROSS', 'F2L', 'OLL', 'PLL']
        self.solve_state = self.states[0]

    def init_colors(self):
        self.colors = self.settings.cube_default_colors

        group_name = self.settings.cube_color_group
        group = self.color_manager.get_color_group(group_name)
        if group != None:
            self.colors.update(group)

        self.colors.update(self.settings.cube_colors)
        print('Color palette:', self.colors)

        default_color = Constants.FALLBACK_COLOR
        for key, value in self.colors.items():
            self.colors[key] = LittleHelpers.convert_hex_color_to_floats(value, default_color)

    def init_mqtt_client(self):
        broker = self.settings.mqtt_client_broker
        port = self.settings.mqtt_client_port
        topic = self.settings.mqtt_client_subscribe_topic
        self.client = MqttClient(broker, port, topic)
        self.client.start()

    def init_opengl(self):
        glutInit()
        glutInitWindowPosition(self.settings.window_position[0], self.settings.window_position[1])
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.settings.window_size[0], self.settings.window_size[1])
        glutCreateWindow(self.settings.window_caption)

        glutReshapeFunc(self.on_reshape_window)
        glutKeyboardFunc(self.on_keyboard_input)
        glutMouseFunc(self.on_mouse_input)
        glutMotionFunc(self.on_mouse_move)
        glutSpecialFunc(self.on_special_input)
        glutVisibilityFunc(self.on_visibility_change)
        glutIdleFunc(self.on_update)
        glutDisplayFunc(self.on_display)

        try:
            if sys.platform == 'linux' or sys.platform == 'linux2':
                glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
            elif sys.platform == 'darwin':
                pass
            elif sys.platform == 'win32':
                pass
        except:
            print("MEH! Something went wrong while setting platform specific code. Let's just ignore this.")

        background_color = LittleHelpers.convert_hex_color_to_floats(self.settings.window_background_color, (0.1, 0.1, 0.1))
        glClearColor(background_color[0], background_color[1], background_color[2], 1)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)#GL_LESS
        glShadeModel(GL_SMOOTH)
        glDisable(GL_LIGHTING)

        if self.settings.texture_mapping_enabled:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    def init_cube(self):
        face_rotation_ease_type = Tween.get_ease_type_by_name(self.settings.cube_face_rotation_ease_type)
        texture_id = self.textures.get(self.settings.texture_mapping_active_texture)
        if texture_id == None:
            texture_id = 0
        self.cube = Cube(self.settings, face_rotation_ease_type, texture_id)
        self.map_cube_colors(self.settings.cube_color_mapping)

    def init_command_handler_map(self):
        self.cmd_handler_map = {
            # standalone commands
            'exit': self.handle_exit_command,
            'quit': self.handle_exit_command,

            'reset_cube': self.handle_reset_cube_command,

            'reset_rotation': self.handle_reset_rotation_command,
            'reset_cube_rotation': self.handle_reset_rotation_command, # obsolete command

            'reset_scale': self.handle_reset_scale_command,
            'reset_cube_scale': self.handle_reset_scale_command, # obsolete command

            'stop_rotation': self.handle_stop_rotation_command,
            'stop_cube_rotation': self.handle_stop_rotation_command, # obsolete command

            'reset_color_mapping': self.handle_reset_color_mapping_command,
            'reset_colors': self.handle_reset_colors,
            'apply_random_pattern': self.handle_apply_random_pattern_command,
            'apply_random_scramble': self.handle_apply_random_scramble_command,

            # commands with one and more parameters
            'map_colors': self.handle_map_colors_command,
            'set_color_orientation': self.handle_map_colors_command, # obsolete command

            'add_rotation_x': self.handle_add_rotation_x_command,
            'add_rotation_y': self.handle_add_rotation_y_command,
            'add_scale': self.handle_add_scale_command,
            'rotate_face': self.handle_rotate_face_command,

            'scramble': self.handle_scramble_command,
            'add_padding': self.handle_add_padding_command,

            'set_background_color': self.handle_set_background_color,
            'load_colors': self.handle_load_colors
        }

    def run(self):
        glutMainLoop()

    def show_gl_info(self):
        print('* GL_RENDERER   : ', glGetString(GL_RENDERER))
        print('* GL_VERSION    : ', glGetString(GL_VERSION))
        print('* GL_VENDOR     : ', glGetString(GL_VENDOR))
        print('* GL_EXTENSIONS : ', glGetString(GL_EXTENSIONS))

    def on_exit(self):
        texture_ids = []
        for name, id in self.textures.items():
            if id:
                texture_ids.append(id)
        if len(texture_ids) > 0:
            print('Deleting textures;', texture_ids)
            glDeleteTextures(texture_ids)

        if self.client:
            self.client.stop()

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
        ch = key.decode('utf-8')

        # exit app on q or ESC:
        if ch == 'q' or ch == chr(self.KEY_ESCAPE):
            sys.exit()
        # reset cube:
        elif ch == chr(self.KEY_BACKSPACE) or ch == chr(self.KEY_DELETE):
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
            self.apply_random_scramble()
        # apply random pattern:
        elif ch == '2':
            self.apply_random_pattern()

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
        elif ch == 's': self.auto_solve('NEXT')
        elif ch == 'S': self.auto_solve('ALL')
        if move != None:
            self.add_moves([move])

    def on_mouse_input(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_drag.begin(x, y)
                self.cube.stop_rotation()
            if state == GLUT_UP:
                self.mouse_drag.end(x, y)

    def auto_solve(self, part='ALL'):
        part = part.upper()
        if type(part) != str:
            return 1

        if part == 'NEXT':
            self.auto_solve(self.solve_state)
            self.solve_state = self.states[self.states.index(self.solve_state) + 1]
        elif part == 'ALL':
            pass
        return

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

    def create_opengl_texture(self, image_size, image_data):
        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, image_size[0], image_size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        return texture_id

    def create_textures(self, image_files):
        for name, filename in image_files.items():
            success, image_size, image_data = LittleHelpers.load_image(filename)
            print('Loaded image:', filename, image_size, success)
            if success:
                texture_id = self.create_opengl_texture(image_size, image_data)
                self.textures[name] = texture_id
        for name, id in self.textures.items():
            print('Created texture:', name, 'with id', id)

    def add_moves(self, moves):
        # print('add_moves', moves)
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        if face_rotations:
            self.append_face_rotations(face_rotations)

    def append_face_rotations(self, face_rotations):
        for face_rotation in face_rotations:
            self.cube.append_face_rotation(face_rotation)

    def scramble_cube(self, moves):
        format_type = type(moves)
        if format_type == list:
            pass
        elif format_type == str:
            moves = moves.split(' ')
        else:
            return
        moves = LittleHelpers.expand_notations(moves)
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        self.cube.scramble(face_rotations)

    def map_cube_colors(self, color_mapping):
        if color_mapping:
            self.color_mapping = color_mapping

        default_color = Constants.FALLBACK_COLOR
        colors = self.colors
        front_color = LittleHelpers.get_mapped_color(Face.FRONT, color_mapping, colors, default_color)
        back_color = LittleHelpers.get_mapped_color(Face.BACK, color_mapping, colors, default_color)
        left_color = LittleHelpers.get_mapped_color(Face.LEFT, color_mapping, colors, default_color)
        right_color = LittleHelpers.get_mapped_color(Face.RIGHT, color_mapping, colors, default_color)
        up_color = LittleHelpers.get_mapped_color(Face.UP, color_mapping, colors, default_color)
        down_color = LittleHelpers.get_mapped_color(Face.DOWN, color_mapping, colors, default_color)
        self.cube.map_colors(front_color, back_color, left_color, right_color, up_color, down_color)

    def reset_cube_color_mapping(self):
        self.map_cube_colors(self.settings.cube_color_mapping)

    def update_cube_color_mapping(self):
        self.map_cube_colors(self.color_mapping)

    def reset_cube_colors(self):
        self.load_colors(self.settings.cube_color_group)

    def set_background_color(self, hex_color):
        color = LittleHelpers.convert_hex_color_to_floats(hex_color)
        if color:
            glClearColor(color[0], color[1], color[2], 1)

    def apply_random_pattern(self):
        pattern = LittleHelpers.get_random_pattern()
        # print('Applying random pattern:', pattern)
        moves = LittleHelpers.expand_notations(pattern.split(' '))
        face_rotations = LittleHelpers.translate_moves_to_face_rotations(moves)
        self.append_face_rotations(face_rotations)

    def apply_random_scramble(self):
        # pattern = LittleHelpers.get_random_pattern()
        pattern = [random.choice(["F","F'","B","B'","R","R'","L","L'","U","U'","D","D'"]) for i in range(40)]
        # print('Applying random scramble:', pattern)
        self.reset_cube()
        self.scramble_cube(pattern)

    def reset_cube(self):
        self.cube.reset()

    def check_message_queue(self):
        if self.client and self.client.has_pending_messages():
            message = self.client.get_next_message()
            if message == None:
                return
            commands = message.strip().split(self.command_delimiter)
            for command in commands:
                self.handle_command(command)

    def load_colors(self, group_name):
        colors = {}
        colors.update(self.colors)

        self.colors = {}
        group = self.color_manager.get_color_group(group_name)
        if group != None:
            self.colors.update(group)
        else:
            return

        self.colors.update(self.settings.cube_colors)
        print('Color palette:', self.colors)

        default_color = Constants.FALLBACK_COLOR
        for key, value in self.colors.items():
            self.colors[key] = LittleHelpers.convert_hex_color_to_floats(value, default_color)

        self.update_cube_color_mapping()

    def handle_command(self, command):
        if not command:
            return

        parts = command.split('=')
        cmd = parts[0].strip()
        params = ''
        if len(parts) >= 2:
            params = parts[1].strip()

        handler = self.cmd_handler_map.get(cmd)
        if handler == None:
            print('Unknown command:', cmd)
            return

        str = 'Processing command: ' + cmd
        if params:
            str += '=' + params
        print(str)
        handler(params)

    def handle_exit_command(self, params):
        sys.exit()

    def handle_reset_cube_command(self, params):
        self.reset_cube()

    def handle_reset_rotation_command(self, params):
        self.cube.reset_rotation()

    def handle_reset_scale_command(self, params):
        self.cube.reset_scale()

    def handle_stop_rotation_command(self, params):
        self.cube.stop_rotation()

    def handle_reset_color_mapping_command(self, params):
        self.reset_cube_color_mapping()

    def handle_reset_colors(self, params):
        self.reset_cube_colors()

    def handle_add_rotation_x_command(self, params):
        if params:
            value = LittleHelpers.convert_str_to_float(params)
            if value != None:
                self.cube.add_rotate_x(value * self.delta_time.elapsed())

    def handle_add_rotation_y_command(self, params):
        if params:
            value = LittleHelpers.convert_str_to_float(params)
            if value != None:
                self.cube.add_rotate_y(value * self.delta_time.elapsed())

    def handle_add_scale_command(self, params):
        if params:
            value = LittleHelpers.convert_str_to_float(params)
            if value != None:
                self.cube.add_scale(value * self.delta_time.elapsed())

    def handle_rotate_face_command(self, params):
        if params:
            moves = LittleHelpers.expand_notations(params.upper().split(' '))
            if len(moves) > 0:
                self.add_moves(moves)

    def handle_apply_random_pattern_command(self, params):
        self.apply_random_pattern()

    def handle_scramble_command(self, params):
        moves = params.upper()
        self.scramble_cube(moves)

    def handle_apply_random_scramble_command(self, params):
        self.apply_random_scramble()

    def handle_map_colors_command(self, params):
        color_mapping = LittleHelpers.make_color_mapping_from_string(params)
        self.map_cube_colors(color_mapping)

    def handle_add_padding_command(self, params):
        if params:
            value = LittleHelpers.convert_str_to_float(params)
            if value != None:
                self.cube.geometry.add_padding(value)

    def handle_set_background_color(self, params):
        if params:
            self.set_background_color(params)

    def handle_load_colors(self, params):
        if params:
            group_name = params
            self.load_colors(group_name)

import pprint
from config import Config

class Settings(Config):
    def __init__(self):
        pass
        # cube settings
        self.cube_draw_cubies = True
        self.cube_draw_sphere = True
        self.cube_draw_lines = False
        self.cube_padding = 0.3
        self.cube_line_width = 2.0
        self.cube_angular_drag = 0.7
        self.cube_scale_drag = 1.2
        self.cube_min_scale = 0.3
        self.cube_max_scale = 1.5
        self.cube_inner_color = [0.0, 0.0, 0.0]
        self.cube_sphere_color = [0.0, 0.0, 0.0]
        self.cube_colors = {
            "blue": [0.066, 0.490, 0.988],
            "orange": [0.996, 0.549, 0.184],
            "green": [0.102, 0.878, 0.133],
            "red": [0.855, 0.082, 0.102],
            "yellow": [0.961, 1.000, 0.204],
            "white": [1.000, 1.000, 1.000]
        }
        self.cube_color_mapping = {
            "front": "blue",
            "back": "green",
            "left": "orange",
            "right": "red",
            "up": "yellow",
            "down": "white",
        }
        self.cube_face_rotation_tween_time = 0.5
        self.cube_face_rotation_ease_type = "ease_cosine"

        # fps settings
        self.fps_update_interval = 10
        self.fps_show = True

        # subscriber settings
        self.subscriber_start = True
        self.subscriber_broker = '127.0.0.1'
        self.subscriber_port = 1883
        self.subscriber_topic = 'pycubix'

        # window settings
        self.window_caption = "PyCubix"
        self.window_width = 600
        self.window_height = 600
        self.window_background_color = [60/255, 67/255, 78/255]

    def load(self, filename):
        print('load_settings', filename)
        config = self.load_json(filename)
        self.assign(config)

    def print(self, config):
        print('# Json')
        i_feel_pretty = pprint.PrettyPrinter(indent=2, width=42, compact=True)
        i_feel_pretty.pprint(config)

    def assign(self, config):
        print('# Settings')
        prop_settings = 'settings'
        prop_cube = 'cube'
        prop_fps = 'fps'
        prop_subscriber = 'subscriber'
        prop_window = 'window'

        if not config or prop_settings not in config:
            return
        settings = config[prop_settings]

        if prop_cube in settings:
            cube = settings[prop_cube]
            self.cube_draw_cubies = self.get_value(cube, ['draw_cubies'], self.cube_draw_cubies)
            self.cube_draw_sphere = self.get_value(cube, ['draw_sphere'], self.cube_draw_sphere)
            self.cube_draw_lines = self.get_value(cube, ['draw_lines'], self.cube_draw_lines)
            self.cube_padding = self.get_value(cube, ['padding'], self.cube_padding)
            self.cube_line_width = self.get_value(cube, ['line_width'], self.cube_line_width)
            self.cube_inner_color = self.get_value(cube, ['inner_color'], self.cube_inner_color)
            self.cube_sphere_color = self.get_value(cube, ['sphere_color'], self.cube_sphere_color)
            self.cube_angular_drag = self.get_value(cube, ['angular_drag'], self.cube_angular_drag)
            self.cube_scale_drag = self.get_value(cube, ['scale_drag'], self.cube_scale_drag)
            self.cube_min_scale = self.get_value(cube, ['min_scale'], self.cube_min_scale)
            self.cube_max_scale = self.get_value(cube, ['max_scale'], self.cube_max_scale)
            self.cube_face_rotation_tween_time = self.get_value(cube['tween'], ['face_rotation_tween_time'], self.cube_face_rotation_tween_time)
            self.cube_face_rotation_ease_type = self.get_value(cube['tween'], ['face_rotation_ease_type'], self.cube_face_rotation_ease_type)
            self.cube_colors = self.get_value(cube, ['colors'], self.cube_colors)
            self.cube_color_mapping = self.get_value(cube, ['color_mapping'], self.cube_color_mapping)

        if prop_fps in settings:
            fps = settings[prop_fps]
            self.fps_update_interval = self.get_value(fps, ['update_interval'], self.fps_update_interval)
            self.fps_show = self.get_value(fps, ['show'], self.fps_show)

        if prop_subscriber in settings:
            subscriber = settings[prop_subscriber]
            self.subscriber_start = self.get_value(subscriber, ['start'], self.subscriber_start)
            self.subscriber_broker = self.get_value(subscriber, ['broker'], self.subscriber_broker)
            self.subscriber_port = self.get_value(subscriber, ['port'], self.subscriber_port)
            self.subscriber_topic = self.get_value(subscriber, ['topic'], self.subscriber_topic)

        if prop_fps in settings:
            fps = settings[prop_fps]
            self.fps_update_interval = self.get_value(fps, ['update_interval'], self.fps_update_interval)

        if prop_window in settings:
            window = settings[prop_window]
            self.window_caption = self.get_value(window, ['caption'], self.window_caption)
            self.window_width = self.get_value(window['size'], ['width'], self.window_width)
            self.window_height = self.get_value(window['size'], ['height'], self.window_height)
            self.window_background_color = self.get_value(window, ['background_color'], self.window_background_color)

    def get_value(self, property, keys, default=None):
        t = property
        for key in keys:
            if key in t:
                t = t[key]
            else:
                t = default
                break
        print('{}: {}'.format(keys[-1], t))
        return t

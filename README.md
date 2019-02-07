# PyCubix

PyCubix is a fork of [PyCube](https://github.com/mtking2/PyCube).

## Purpose

To be determined.

## Dependencies

Glut:
- `$ sudo apt install freeglut3 freeglut3-dev`

Paho MQTT:
- `$ sudo apt install mosquitto mosquitto-clients`

The following Python modules are needed to run this program:
- [NumPy](http://www.numpy.org/)
- [PyOpenGL](pyopengl.sourceforge.net/), see also [OpenGL](https://www.opengl.org/)
- [Paho MQTT](https://pypi.org/project/paho-mqtt/), see also [Eclipse Paho](https://www.eclipse.org/paho/)

## Installation

### Install using pip

Python 3.x: `$ pip3 install numpy pyopengl`

### Install using Virtualenv and make

- `$ cd PyCubix`
- `$ virtualenv -p python3 env`
- `$ source env/bin/activate`
- `$ make install`

## Running the program

### Just do it

- `$ cd PyCubix`
- `$ python src/main.py`

### Run using Virtualenv and make

- `$ cd PyCubix`
- `$ source venv/bin/activate`
- `$ make run` or simply `$ make`

## Usage:

- F, R, U, B, L, D: Rotate face in clockwise direction
- SHIFT + F, R, U, B, L, D: Rotate face in counter clockwise direction
- Use the ARROW keys to rotate the cube
- SPACE stops the rotation
- RETURN resets the rotation
- Use +/- to scale the cube
- BACKSPACE resets the cube geometry
- Use '1' to instantly apply a random pattern
- Use '2' to apply a random pattern (you should probably reset the cube geometry first if the cube is already scrambled)
- Use the mouse to rotate the cube around the x- and the y-axis

## Customization

Some parts of the application are customizable with a config file in `cfg/settings.json`. The default values are as follows and can also be found in `cfg/no-touch.json`. Just in case.

```
{
    "settings": {
        "cube": {
            "draw_cubies": true,
            "draw_sphere": true,
            "draw_lines": false,
            "padding": 0.3,
            "line_width": 4,
            "angular_drag": 0.7,
            "scale_drag": 4.2,
            "scaling": {
                "min": 0.3,
                "max": 1.5
            },
            "initial_rotation": {
                "x_angle": 0,
                "y_angle": 0
            },
            "inner_color": [0.0, 0.0, 0.0],
            "sphere_color": [0.0, 0.0, 0.0],
            "tween": {
                "face_rotation_tween_time": 0.5,
                "face_rotation_ease_type": "ease_cosine"
            },
            "colors": {
                "blue": [0.066, 0.490, 0.988],
                "orange": [0.996, 0.549, 0.184],
                "green": [0.102, 0.878, 0.133],
                "red": [0.855, 0.082, 0.102],
                "yellow": [0.961, 1.000, 0.204],
                "white": [1.000, 1.000, 1.000]
            },
            "color_mapping": {
                "front": "blue",
                "back": "green",
                "left": "orange",
                "right": "red",
                "up": "yellow",
                "down": "white"
            },
            "auto_rotation": {
                "x_axis": {
                    "enabled": false,
                    "begin_angle": -30,
                    "end_angle": 30,
                    "time": 8,
                    "ease_type": "ease_cosine",
                    "jump_start": 0.5
                },
                "y_axis": {
                    "enabled": false,
                    "begin_angle": 135,
                    "end_angle": -135,
                    "time": 16,
                    "ease_type": "ease_cosine",
                    "jump_start": 0.5
                }
            }
        },
        "fps": {
            "show": true,
            "update_interval": 30
        },
        "mouse": {
            "sensitivity": 5
        },
        "mqtt_client": {
            "start": true,
            "broker": "127.0.0.1",
            "port": 1883,
            "subscribe_topic": "pycubix",
            "publish_topic": "pycubix_out"
        },
        "window": {
            "caption": "PyCubix",
            "background_color": [0.203, 0.239, 0.274],
            "size": {
                "width": 600,
                "height": 600
            }
        }
    }
}
```

## Using MQTT to send commands to the cube

### Installation

`$ sudo apt-get install mosquitto mosquitto-clients`

See also [How to Install and Secure the Mosquitto MQTT Messaging Broker](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04)

### Publish (send) a message to the application via a terminal

`$ mosquitto_pub -h localhost -t pycubix -m "add_rotation_x = 0.73"`

Where -h is used to specify the hostname of the MQTT server and -t is the name of the topic.

Using `iot.eclipse.org` for instance also works fine as a host.

### Supported commands

Standalone commands:
- `reset_cube`: Reset the cube (geometry and color orientation)
- `reset_rotation`: Reset the cube's rotation
- `reset_scale`: Reset the cube's scale
- `reset_color_mapping`: Reset the cube's color mapping
- `stop_rotation`: Stop the cube's rotation
- `apply_random_pattern`: Apply a random pattern from the pattern database (***)
- `apply_random_scramble`: Apply a random scramble
- `quit` or `exit`: Quit/exit application

Commands with parameters:
- `add_rotation_x = <float_value>`: Rotate the cube around the x axis. Example: `add_rotation_x = 0.11`
- `add_rotation_y = <float_value>`: Rotate the cube around the y axis. Example: `add_rotation_y = 0.29`
- `add_scale = <float_value>`: Scale the cube. Example: `add_scale = 0.73`
- `rotate_face = <list_of_faces_to_be_rotated>`: Rotate one or more faces of the cube using the Rubik's cube notation. The cube is not reset before executing the moves. Example: `rotate_face = R U R' U'`
- `map_colors = <list_of_face_to_color_mappings>`. Apply a color (blue, red, yellow, green, orange, white) to a face (front, right, up, back, left, down). Example: `map_colors = front:blue, back:green, left:red, right:orange, up:white, down:yellow`
- `scramble = <list_of_faces_to_be_rotated>`: Scramble the cube with a given algorithm/list of moves. It practically works as the rotate_face command, but the cube the faces are rotated INSTANTLY (within the same frame), meaning that the face rotations are not being shown/animated/tweened. Example: `scramble = R U R' U'`. To maintain a prior applied color orientation, you would do the follow to scramble the cube: `reset_cube;set_color_orientation = front:blue, back:green, left:red, right:orange, up:white, down:yellow;scramble = U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2`.
- `add_padding = <float_value>`: Modify the padding between the cubies. Example: `add_padding = 0.5`. (NOTE: This method has a bug and does only work correctly when the padding is applied BEFORE the first face rotation.)
- `set_background_color = <float_value_red>, <float_value_green>, <float_value_blue>`: Set the windows's background color. Example: `set_background_color = 0.3, 0.3, 0.3`

It's also possible more than one command in a single message. The commands need to be separated by a semicolon though. Example: `reset_cube;apply_random_pattern`

## What else is there?

### List of known notations

- Front face: F F' F2 F2'
- Back face: B B' B2 B2'
- Left face: L L' L2 L2'
- Right face: R R' R2 R2'
- Up face: U U' U2 U2'
- Down face: D D' D2 D2'

Wide movements (like Fw) as well as M, E, S, x, y, z are not supported at the moment.

## Tested on the following operating systems

- Ubuntu 18.04
- Raspbian 9 (Stretch)

*** The database is a lie.

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
- Use '0' to reorient the colors (in this test case, white is applied to the UP face and so forth)
- Mouse support isn't implemented yet

## Customization

Some parts of the application are customizable with a config file in `cfg/settings.json`. The default values are as follows and can also be found in `cfg/no-touch.json`. Just in case.

`{
    "settings": {
        "subscriber": {
            "start": true,
            "broker": "127.0.0.1",
            "port": 1883,
            "topic": "pycubix"
        },
        "fps": {
            "update_interval": 10
        },
        "window": {
            "caption": "PyCubix",
            "background_color": [0.235, 0.263, 0.306],
            "size": {
                "width": 600,
                "height": 600
            }
        },
        "cube": {
            "draw_stickers": true,
            "draw_sphere": true,
            "draw_lines": false,
            "padding": 0.3,
            "line_width": 4,
            "face_rotation_tween_time": 0.5,
            "inner_color": [0.0, 0.0, 0.0],
            "sphere_color": [0.0, 0.0, 0.0],
            "color_orientation_string": "front:blue, back:green, right:red, left:orange, up:yellow, down:white",
            "face_colors": {
                "blue": [0.066, 0.490, 0.988],
                "orange": [0.996, 0.549, 0.184],
                "green": [0.102, 0.878, 0.133],
                "red": [0.855, 0.082, 0.102],
                "yellow": [0.961, 1.000, 0.204],
                "white": [1.000, 1.000, 1.000]
            }
        }
    }
}`

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
- `reset_cube_rotation`: Reset the cube's rotation
- `reset_cube_scale`: Reset the cube's scale
- `stop_cube_rotation`: Stop the cube's rotation
- `apply_random_pattern`: Apply a random pattern from the pattern database (***)
- `quit` or `exit`: Quit/exit application

Commands with parameters:
- `add_rotation_x = <float_value>`: Rotate the cube around the x axis. Example: `add_rotation_x = 0.11`
- `add_rotation_y = <float_value>`: Rotate the cube around the y axis. Example: `add_rotation_y = 0.29`
- `rotate_face = <list_of_faces_to_be_rotated>`: Rotate one or more faces of the cube using the Rubik's cube notation. The cube is not reset before executing the moves. Example: `rotate_face = R U R' U'`
- `scramble = <list_of_faces_to_be_rotated>`: Scramble the cube with a given algorithm/list of moves. It practically works as the rotate_face command, but the cube is reset first and then the faces are rotated INSTANTLY (within the same frame), meaning that the the face rotations are not being shown/animated/tweened. Example: `scramble = R U R' U'`
- `set_color_orientation = <list_of_face_to_color_mappings>`. Apply a color (blue, red, yellow, green, orange, white) to a face (front, right, up, back, left, down). Example: `set_color_orientation = front:blue, back:green, left:red, right:orange, up:white, down:yellow`

It's also possible to put more than one command in a single message. The commands need to be separated by a semicolon though. Example: `reset_cube;apply_random_pattern`

## What else is there?

### List of known notations

- Front face: F F' F2
- Back face: B B' B2
- Left face: L L' L2
- Right face: R R' R2
- Up face: U U' U2
- Down face: D D' D2

Wide movements (like Fw) as well as M, E, S, x, y, z are not supported at the moment.

## Tested on the following operating systems

- Ubuntu 18.04
- Raspbian 9 (Stretch)

*** The database is a lie.


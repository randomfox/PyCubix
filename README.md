# PyCubix

This is a fork of mtking2's [PyCube](https://github.com/mtking2/PyCube).

## Intention

To build a [digital twin](https://en.wikipedia.org/wiki/Digital_twin) of a Rubik's cube which can be controlled remotely with a small set of commands.

## Result

In the end, the digital twin was running on a Raspberry Pi and received its commands via MQTT from a [BrickPi](https://www.dexterindustries.com/brickpi/) which was solving the Rubik's cube.

<img src="https://github.com/grumpypixel/Readme-Resources/blob/master/PyCubix/pycubix-on-rpi.png" width="800">

<img src="https://github.com/grumpypixel/Readme-Resources/blob/master/PyCubix/pastel-cube-hi-all-around.gif" width="400">

See also:
- [Pimp My Twin](https://medium.com/@pwc.emtech.eu/pimp-my-twin-83947430281)
- [Creating a Digital Twin Showcase](https://medium.com/@pwc.emtech.eu/creating-a-digital-twin-showcase-4ad0895fd30e)

## Dependencies

GLUT - the OpenGL Utility Toolkit:
- `$ sudo apt-get install freeglut3 freeglut3-dev`

Paho MQTT (optional):
- `$ sudo apt-get install mosquitto mosquitto-clients`

The following Python modules are needed to run this program:
- [NumPy](http://www.numpy.org/)
- [Paho MQTT](https://pypi.org/project/paho-mqtt/), see also [Eclipse Paho](https://www.eclipse.org/paho/)
- [Pillow](https://pypi.org/project/Pillow/), see also [Pillow homepage](https://python-pillow.org/)
- [PyOpenGL](pyopengl.sourceforge.net/), see also [OpenGL](https://www.opengl.org/)

## Installation

### Install using pip

Python 3.x: `$ pip3 install numpy paho-mqtt pillow pyopengl`

### Install using Virtualenv and make

- `$ cd PyCubix`
- `$ virtualenv -p python3 env`
- `$ source env/bin/activate`
- `$ make install`

## Running the program

### Just do it!

- `$ cd PyCubix`
- `$ python src/main.py`
or
- `$ python src/main.py --settings cfg/settings.json --colors cfg/colors.json`

### Run using Virtualenv and make

- `$ cd PyCubix`
- `$ source venv/bin/activate`
- `$ make run` or simply `$ make`

## Usage

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

### Customizable settings

Some parts of the application are customizable and can be set in `cfg/settings.json`:

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
            "inner_color": "#000000",
            "sphere_color": "#000000",
            "tween": {
                "face_rotation_tween_time": 0.5,
                "face_rotation_ease_type": "ease_cosine"
            },
            "color_group": "material",
            "colors": {
                "black": "#000000",
                "blue": "#00A0D1",
                "cyan": "#00FFFF",
                "magenta": "#FF00FF"
            },
            "color_mapping": {
                "front": "green",
                "back": "blue",
                "left": "orange",
                "right": "red",
                "up": "white",
                "down": "yellow"
            },
            "auto_rotation": {
                "x_axis": {
                    "enabled": true,
                    "begin_angle": -30,
                    "end_angle": 30,
                    "time": 8,
                    "ease_type": "ease_cosine",
                    "jump_start": 0.5
                },
                "y_axis": {
                    "enabled": true,
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
        "resources": {
            "images": {
                "rounded-sticker": "res/sticker-rounded.jpg",
                "squared-sticker": "res/sticker-squared.jpg",
                "no-sticker": "res/stickerless.jpg"
            }
        },
        "texture_mapping": {
            "enabled": true,
            "active_texture": "rounded-sticker"
        },
        "window": {
            "caption": "PyCubix",
            "background_color": "#343D46",
            "position": {
                "x": 0,
                "y": 0
            },
            "size": {
                "width": 600,
                "height": 600
            }
        }
    }
}
```

### Pimp my colors

The colors are also pimpable in `cfg/colors.json`:

```
{
    "colors": {
        "default": {
            "blue": "#004BAB",
            "orange": "#FF5623",
            "yellow": "FFD22C",
            "green": "#009A4A",
            "red": "#BE0F38",
            "white": "#FFFFFF"
        },
        "material": {
            "blue": "#2962FF",
            "orange": "#FF6D00",
            "yellow": "#FFD600",
            "green": "#00C853",
            "red": "#D50000",
            "white": "#FFFFFF"
        },
        "pastel": {
            "blue": "#2FB3EC",
            "orange": "#DF439E",
            "yellow": "#FFBE4C",
            "green": "#83DD52",
            "red": "#FF4931",
            "white": "#FFFFFF"
        },
        "six_shades_of_purple": {
            "blue": "#BA55D3",
            "orange": "#EE82EE",
            "yellow": "#8B008B",
            "green": "#FF00FF",
            "red": "#DA70D6",
            "white": "#DDA0DD"
        }
    }
}
```

### Additional notes

Colors from the colors-property in cfg/settings.json will extend/overwrite the colors taken from the color group in cfg/colors.json.

## Using MQTT to send commands to the cube

### Installation

`$ sudo apt-get install mosquitto mosquitto-clients`

See also [How to Install and Secure the Mosquitto MQTT Messaging Broker](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04)

### Publish (send) a message to the application via a terminal

`$ mosquitto_pub -h localhost -t pycubix -m "add_rotation_x = 0.73"`

Where -h is used to specify the hostname of the MQTT server and -t is the name of the topic.

Using `iot.eclipse.org` as a host for testing purposes also works fine.

### Supported commands

Standalone commands:
- `reset_cube`: This command resets the geometry, stops the current tween and clears the queued face rotations. It does neither reset the color mapping nor the cube's rotation or scale.
- `reset_rotation`: Reset the cube's rotation
- `reset_scale`: Reset the cube's scale
- `reset_color_mapping`: Reset the cube's color mapping
- `reset_colors`: Reset the cube's colors
- `stop_rotation`: Stop the cube's rotation
- `apply_random_pattern`: Apply a random pattern from the pattern database (***)
- `apply_random_scramble`: Scramble the cube with a random pattern
- `quit` or `exit`: Quit/exit application

Commands with parameters:
- `add_rotation_x = <float_value>`: Rotate the cube around the x axis. Example: `add_rotation_x = 0.11`
- `add_rotation_y = <float_value>`: Rotate the cube around the y axis. Example: `add_rotation_y = 0.29`
- `add_scale = <float_value>`: Scale the cube. Example: `add_scale = 0.73`
- `rotate_face = <list_of_faces_to_be_rotated>`: Rotate one or more faces of the cube using the Rubik's cube notation. The cube is not reset before executing the moves. Example: `rotate_face = R U R' U'`
- `map_colors = <list_of_face_to_color_mappings>`. Apply a color (blue, red, yellow, green, orange, white) to a face (front, right, up, back, left, down). Example: `map_colors = front:blue, back:green, left:red, right:orange, up:white, down:yellow`
- `scramble = <list_of_faces_to_be_rotated>`: Scramble the cube with a given algorithm/list of moves. It practically works as the rotate_face command, but the cube the faces are rotated INSTANTLY (within the same frame), meaning that the face rotations are not being shown/animated/tweened. Example: `scramble = R U R' U'`. To maintain a prior applied color orientation, you would do the follow to scramble the cube: `reset_cube;set_color_orientation = front:blue, back:green, left:red, right:orange, up:white, down:yellow;scramble = U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2`
- `add_padding = <float_value>`: Modify the padding between the cubies. Example: `add_padding = 0.5` (NOTE: This method is not implemented correctly and does only work as expected when the padding is applied BEFORE the first face rotation)
- `load_colors = <color_group_name>`: Load colors by its group name and apply them instantly. Example: `load_colors = default`
- `set_background_color = <hex_color>`: Set the background color of the window. Example: `set_background_color = #303030` (the '#' can be omitted though)

It's also possible to send more than one command in a single message. The commands need to be separated by a semicolon though. Example: `reset_cube;apply_random_pattern`

## What else is there?

### List of known notations

- Front face: F F' F2 F2'
- Back face: B B' B2 B2'
- Left face: L L' L2 L2'
- Right face: R R' R2 R2'
- Up face: U U' U2 U2'
- Down face: D D' D2 D2'

Wide moves like Rw as well as M, E, S, x, y, z are not supported at the moment.

## Tested on the following operating systems

- Ubuntu 18.04
- Raspbian 9 (Stretch)
- macOS 10.14

*** The database is a lie.

# PyCubix

PyCubix is a fork of [PyCube](https://github.com/mtking2/PyCube).

## Purpose

To be determined.

## Dependencies

Glut:
- `sudo apt install freeglut3 freeglut3-dev`

The following Python modules are needed to run this program:
- [NumPy](http://www.numpy.org/)
- [PyOpenGL](pyopengl.sourceforge.net/) see also [OpenGL](https://www.opengl.org/)

## Installation

### Install using pip

Python 3.x: `pip3 install numpy pyopengl`

### Install using Virtualenv and make

- `cd PyCubix`
- `virtualenv -p python3 env`
- `source env/bin/activate`
- `make install`

## Running the program

### Just do it

- `cd PyCubix`
- `python src/main.py`

### Run using Virtualenv and make

- `cd PyCubix`
- `source venv/bin/activate`
- `make run` or simply `make`

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
            "line_width": 2,
            "sphere_color": [0, 0, 0],
            "face_rotation_tween_time": 0.5
        }
    }
}`

## MQTT, commands and stuff

This is still work in progress.

## Tested on the following systems
- Ubuntu 18.04
- Raspberry Pi

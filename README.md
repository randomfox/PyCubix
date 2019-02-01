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

## Install using pip

Python 3.x: `pip3 install numpy pyopengl`

## Install using Virtualenv and make

- `cd PyCubix`
- `virtualenv -p python3 venv`
- `source venv/bin/activate`
- `make install`

## Run the program

- `cd PyCubix`
- `python src/main.py`

## Run using Virtualenv

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
- Mouse support isn't implemented yet

## Tested on the following systems
- Ubuntu 18.04
- Raspberry Pi

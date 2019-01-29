# PyCubix

PyCubix is a fork of [PyCube](https://github.com/mtking2/PyCube) originally written by [mtking2](https://github.com/mtking2).

## Purpose

To be determined.

## Dependencies

Glut:
- `sudo apt install freeglut3 freeglut3-dev`

The following Python modules are needed to run this program:
[NumPy](http://www.numpy.org/)
[PyOpenGL](pyopengl.sourceforge.net/) see also [OpenGL](https://www.opengl.org/)

## Install Python modules using pip

Python 3.x: `pip3 install numpy pyopengl`

## Run the program

- `cd PyCubix`
- `python src/main.py`

## Install modules and run using Virtualenv and make

- `cd PyCubix`
- `virtualenv -p python3 venv`
- `source venv/bin/activate`
- `make install`
- `make run`

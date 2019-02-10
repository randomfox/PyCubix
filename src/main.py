import argparse
import colorsys

from app import App
from colormanager import ColorManager
from settings import Settings

parser = argparse.ArgumentParser()
parser.add_argument('--settings', help='Path to settings file', required=False)
parser.add_argument('--colors', help='Path to colors file', required=False)
parser.add_argument('--glinfo', help='Show OpenGL info', required=False, action="store_true")
args = parser.parse_args()

# parse colors
colors_file = 'cfg/colors.json'
if args.colors != None:
	colors_file = args.colors
color_manager = ColorManager()
color_manager.load(colors_file)

# parse settings
settings_file = 'cfg/settings.json'
if args.settings != None:
	settings_file = args.settings
settings = Settings()
settings.load(settings_file)

display_glinfo = args.glinfo
app = App(settings, color_manager, display_glinfo)
app.run()

#!/usr/bin/env python3

"""Shoes placed
Make Vector place shoes for us.
"""
import io
import os
import sys
import time
import random
try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Imports the Anki Vector SDK
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps

robot = anki_vector.Robot(
    anki_vector.util.parse_command_args().serial, enable_camera_feed=True)
screen_dimensions = anki_vector.screen.SCREEN_WIDTH, anki_vector.screen.SCREEN_HEIGHT


def find_object():
    print('Looking for object.')


def place_object():
    print('Place object.')
    robot.behavior.drive_straight(distance_mm(50), speed_mmps(50))
    robot.behavior.turn_in_place(degrees(90))


def connect_robot():
    print('Connect to Vector...')
    robot.connect()


def disconnect_robot():
    robot.disconnect()
    print('Vector disconnected')


def stand_by():
    # If necessary, move Vector's Head and Lift to make it easy to see his face
    robot.behavior.set_lift_height(0.0)


def show_camera():
    print('Show camera')
    robot.camera.init_camera_feed()
    robot.vision.enable_display_camera_feed_on_face(True)


def close_camera():
    print('Close camera')
    robot.vision.enable_display_camera_feed_on_face(False)
    robot.camera.close_camera_feed()


def save_image(file_name):
    print('Save image')
    robot.camera.latest_image.save(file_name, 'JPEG')


def show_image(file_name):
    print('Show image = {}'.format(file_name))

    # Load an image
    image = Image.open(file_name)

    # Convert the image to the format used by the Screen
    print("Display image on Vector's face...")
    screen_data = anki_vector.screen.convert_image_to_screen_data(
        image.resize(screen_dimensions))
    robot.screen.set_screen_with_image_data(screen_data, 5.0, True)


def robot_say(text):
    print('Say {}'.format(text))
    robot.say_text(text)


def place_shoes():
    stand_by()
    show_camera()
    robot_say('My lord, Let me place shoes for you.')

    robot_say('Start to look for shoes')
    find_object()
    time.sleep(2)

    robot_say('Start to place right shoes')
    place_object()
    time.sleep(2)

    robot_say('Start to place left shoes')
    place_object()
    time.sleep(2)

    close_camera()
    robot_say('Shoes placed, done, goodbye!')


def main():
    connect_robot()
    try:
        place_shoes()
    except Exception as e:
        print('Analyze Exception: {}', e)

    disconnect_robot()


if __name__ == "__main__":
    main()

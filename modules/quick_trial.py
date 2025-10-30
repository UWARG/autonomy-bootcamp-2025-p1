"""
Runs colour detection on sample image.
"""

import pathlib
import os

# debug modules.detect_colours import ... not being found
# import sys

# print(f"Current Working Directory: {os.getcwd()}")
# print("\nPython Path (where Python looks for modules):")
# for path in sys.path:
#     print(f"- {path}")

from modules.detect_colours import DetectBlue, DetectRed


# Output results of colour detections
OUTPUT_PATH = pathlib.Path("Output")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
IMAGE = "map_test.jpg"

# fix relative path error
script_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(script_dir, IMAGE)


# labels for red and blue colour detections
BLUE_DETECTION = OUTPUT_PATH / "blue_colour_detection.jpg"
RED_DETECTION = OUTPUT_PATH / "red_colour_detection.jpg"

blue_detector = DetectBlue.create()
red_detector = DetectRed.create()

blue_detector.run(IMAGE, BLUE_DETECTION)
red_detector.run(IMAGE, RED_DETECTION)

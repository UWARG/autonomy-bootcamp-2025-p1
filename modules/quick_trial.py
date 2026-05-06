"""
Runs colour detection on sample image.
"""

import pathlib
import time

from detect_colours import DetectBlue, DetectRed


# Output results of colour detections
OUTPUT_PATH = pathlib.Path("Output")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
IMAGE = "map_test.jpg"

# labels for red and blue colour detections
BLUE_DETECTION = OUTPUT_PATH / f"blue_colour_detection_{time.time_ns()}.jpg"
RED_DETECTION = OUTPUT_PATH / f"red_colour_detection_{time.time_ns()}.jpg"

blue_detector = DetectBlue.create()
red_detector = DetectRed.create()

blue_detector.run(IMAGE, BLUE_DETECTION)
red_detector.run(IMAGE, RED_DETECTION)

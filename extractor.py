#!/usr/bin/env python3

import sys
from os import path
import json

from PIL import Image
from tesserocr import PyTessBaseAPI, RIL


# Translate a point
# from Cartesian to the screen coordinate system
def pointToScreen(pointInCart, height):
    return pointInCart[0], height - pointInCart[1]

def expectedSlope(desc, image):
    _, height = image.size

    try:
        desc_start = desc["start"]
    except KeyError:
        return None

    start = pointToScreen(desc_start, height)
    end = pointToScreen(desc["end"], height)
    return (end[1] - start[1]) / \
        (end[0] - start[0])


# A JSON file specifying test images and the expected results
test_params_file = sys.argv[2]
# The directory with the images referred to in test_params_file
image_root = sys.argv[1]

threshold = 0.005

passed = 0
failed = 0

with open(path.join(image_root, test_params_file), "r") as f:
    images = json.load(f)

with PyTessBaseAPI() as api:
    for i in images:
        imagePath = path.join(image_root, i["file"])
        print(imagePath)
        image = Image.open(imagePath)

        expected = expectedSlope(i, image)

        try:
            api.SetImage(image)
        except RuntimeError:
            print("Couldn't read", imagePath, ", skipping.")
            continue
        
        _, _, _, obtained = api.AnalyseLayout().Orientation()

        print("expected:", expected,
              ", obtained:", obtained)
        if expected is None:
            continue

        if abs(expected - obtained) <= threshold:
            passed += 1
            print("pass")
        else:
            failed += 1
            print("FAIL")

print("passed:", passed,
      ", failed:", failed,
      ", success rate:", passed / (failed + passed))

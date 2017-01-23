#!/usr/bin/env python3

from os import path
import json

from PIL import Image
from tesserocr import PyTessBaseAPI, RIL


def pointToTL(pointInCart, height):
    #return pointInCart
    return pointInCart[0], height - pointInCart[1]

def expectedSlope(desc, image):
    _, height = image.size

    try:
        desc_start = desc["start"]
    except KeyError:
        return None

    start = pointToTL(desc_start, height)
    end = pointToTL(desc["end"], height)
    return (end[1] - start[1]) / \
        (end[0] - start[0])

root = "../final-test-set"

threshold = 0.01

passed = 0
failed = 0

with open(path.join(root, "first-sample-test-slopes.json"), "r") as f:
    images = json.load(f)

with PyTessBaseAPI() as api:
    for i in images:
        imagePath = path.join(root, i["file"])
        print(imagePath)
        image = Image.open(imagePath)

        expected = expectedSlope(i, image)

        try:
            api.SetImage(image)
        except RuntimeError:
            continue
        
        # boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        # print(boxes)
        # for (im, box, _, _) in boxes:
        #     api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
        #     text = api.GetUTF8Text()
        #     if text == "":
        #         print("Text is empty")
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

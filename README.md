# text-slope-extractor

A script evaluating Tesseract's skew angle detection.

A test set can be found at https://drive.google.com/drive/folders/0B_UhOpJxnOKQazBYVUV4TkZlZEU?usp=sharing .

Run with:
```
. ./.venv/bin/activate
./extractor.py final-test-set/first-sample-test.json 0.01
```
Arguments:
 1. the test description file
 2. the success threshold - if the difference between the expected 
    and the obtained text slopes is `<= threshold`, 
	it's considered a success.


## Test description file

A test description file specifies test images and the expected results.
It is a JSON file of the form:

```
[
	{
		"start": line_start,
		"end": line_end,
		"picture": null | [picture_top_left, picture_bottom_right]
		"file": relative_image_path
	},
	
	...
]
```

Where:

 - `line_{start,end}` are the endpoints of a line describing the text line slope
 - `picture_{top_left,bottom_right}` are the corners of the picture
   in the image. Currently they are ignored.
 - `relative_image_path` is the path to the test image
   relative to the description file

Points are of the form `[x, y]` and are in Cartesian coordinates (`y` starts from the bottom). Such coordinates can be obtained from Inkscape.

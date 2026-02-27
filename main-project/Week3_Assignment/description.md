Assignment 3: Lane Detection using Edge Detection and Hough Transform

Objective

You are required to implement a lane detection algorithm using Edge Detection and the Hough Transform. This assignment aims to simulate how autonomous vehicles detect lane markings.

Task Description

Input: 10 images representing road scenes as if captured from a car-mounted camera.
Output: 10 corresponding images with detected lane lines (1 or 2 lanes) clearly visualized.
Core Techniques:
Edge Detection (use Canny Edge Detector)
Hough Transform (Line detection)
Parameter Tuning:
Adjust the two thresholds of the Canny Edge Detector for optimal results.
Experiment and fine-tune Hough Transform parameters to best visualize the lane lines.
Note: You must write one Python program that processes all 10 input images using the same code base (do not write separate code for each image). 10 input images can be proceeded separately but with only one source code.

Assignment Requirements

Code Implementation:
Load each of the 10 images.
Apply the Canny Edge Detector. You must fine-tune its two threshold parameters for quality edge detection.
Apply the Hough Transform to detect lane lines. Adjust its parameters as necessary to ensure robust line detection.
Overlay the detected lane lines onto the original images and save the results.
Report:
Include a link to your code repository on Github.
Insert all 10 output images, each showing the detected lane(s) on the original road scenes.
Briefly summarize the parameter values you used and discuss any challenges faced and how you overcame them.
(Optional: Extension)
For extra credit, add code that marks the “center” of the detected lane (e.g., the midpoint between two detected lanes). Illustrate this by drawing a circle at that location on each output image.
 

Submission

Upload your report as a PDF or docx file.
Insert the working Github link.
All 10 output images must be clearly labeled and shown in your report.
If you do the optional part, describe and illustrate your approach as well.
 

Hints

Consider ROI (Region of Interest) masking to focus detection on the road area.
You may use Python and OpenCV for image processing tasks.
Test your code thoroughly to ensure that it works for all 10 images.
# CS4375 - Producer Consumer Lab
--
*by super anonymous student, last update November 18th, 2018*
## Overview
This lab implements a simple producer/consumer queue exercise. The lab takes the provided video clip (clip.mp4) and, using OpenCV, converts each frame to grayscale and displays the frames at about 24 frames per second. In one thread, frames are extracted from the clip one by one, placed into a buffer, from which another thread reads the frames and converts each one to grayscale. Each grayscale frame is then placed into another buffer, which is read from another thread to display the frames. Each buffer, by default, has a maximum size of 10. Additionally, the start order of the threads is shuffled upon running the lab.

Note that on macOS, OpenCV's `imshow` method only works on the main thread.

A copy of the original assignment prompt is in ASSIGNMENT.md.

## Running Instructions
To run the lab, simply download or clone the repository and run the server script using `python3`. For example:

`python3 lab.py` or `./lab.py`

## Prerequisites
In order to run this lab, it's necessary to have the Python 3 OpenCV bindings. These can be installed via pip with

`pip install opencv-python`

## References
Much of the code for reading frames, converting to grayscale, and then displaying frames at 24 FPS was provided by the course team.

I referenced this StackOverflow post for how to create Python threads without writing new classes. (https://stackoverflow.com/questions/2905965/creating-threads-in-python)

I also referenced the Wikipedia page for Producer-Consumer. (https://en.wikipedia.org/wiki/Producer–consumer_problem)


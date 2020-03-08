# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""An annotation library that draws overlays on the Pi camera preview.

Annotations include bounding boxes and text overlays.
Annotations support partial opacity, however only with respect to the content in
the preview. A transparent fill value will cover up previously drawn overlay
under it, but not the camera content under it. A color of None can be given,
which will then not cover up overlay content drawn under the region.
Note: Overlays do not persist through to the storage layer so images saved from
the camera, will not contain overlays.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
from PIL import ImageDraw


import subprocess #for espeak
from string import digits  #to remove digits from string
import re
res=0

import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
    
    

def _round_up(value, n):
  """Rounds up the given value to the next number divisible by n.

  Args:
    value: int to be rounded up.
    n: the number that should be divisible into value.

  Returns:
    the result of value rounded up to the next multiple of n.
  """
  return n * ((value + (n - 1)) // n)


def _round_buffer_dims(dims):
  """Appropriately rounds the given dimensions for image overlaying.

  As per the PiCamera.add_overlay documentation, the source data must have a
  width rounded up to the nearest multiple of 32, and the height rounded up to
  the nearest multiple of 16. This does that for the given image dimensions.

  Args:
    dims: image dimensions.

  Returns:
    the rounded-up dimensions in a tuple.
  """
  width, height = dims
  return _round_up(width, 32), _round_up(height, 16)


class Annotator:
  """Utility for managing annotations on the camera preview."""

  def __init__(self, camera, default_color=None):
    """Initializes Annotator parameters.

    Args:
      camera: picamera.PiCamera camera object to overlay on top of.
      default_color: PIL.ImageColor (with alpha) default for the drawn content.
    """
    self._camera = camera
    self._dims = camera.resolution
    self._buffer_dims = _round_buffer_dims(self._dims)
    self._buffer = Image.new('RGBA', self._buffer_dims)
    self._overlay = None
    self._draw = ImageDraw.Draw(self._buffer)
    self._default_color = default_color or (0xFF, 0, 0, 0xFF)

  def update(self):
    """Draws any changes to the image buffer onto the overlay."""
    # For some reason, simply updating the current overlay causes
    # PiCameraMMALError every time we update. To avoid that, we create a new
    # overlay each time we want to update.
    # We use a temp overlay object because if we remove the current overlay
    # first, it causes flickering (the overlay visibly disappears for a moment).
    temp_overlay = self._camera.add_overlay(
        self._buffer.tobytes(), format='rgba', layer=3, size=self._buffer_dims)
    if self._overlay is not None:
      self._camera.remove_overlay(self._overlay)
    self._overlay = temp_overlay
    self._overlay.update(self._buffer.tobytes())

  def clear(self):
    """Clears the contents of the overlay, leaving only the plain background."""
    self._draw.rectangle((0, 0) + self._dims, fill=(0, 0, 0, 0x00))
    #subprocess.call(['espeak',str(res)])
    

  def bounding_box(self, rect, outline=None, fill=None):
    """Draws a bounding box around the specified rectangle.

    Args:
      rect: (x1, y1, x2, y2) rectangle to be drawn, where (x1, y1) and (x2, y2)
        are opposite corners of the desired rectangle.
      outline: PIL.ImageColor with which to draw the outline (defaults to the
        Annotator default_color).
      fill: PIL.ImageColor with which to fill the rectangle (defaults to None,
        which will *not* cover up drawings under the region).
    """
    outline = outline or self._default_color
    self._draw.rectangle(rect, fill=fill, outline=outline)

  def text(self, location, text, color=None):
    """Draws the given text at the given location.

    Args:
      location: (x, y) point at which to draw the text (upper left corner).
      text: string to be drawn.
      color: PIL.ImageColor to draw the string in (defaults to the Annotator
        default_color).
    """
    color = color or self._default_color
    self._draw.text(location, text, fill=color)
    
    ini_string = text
    remove_digits = str.maketrans('', '', digits)
    res = ini_string.translate(remove_digits) 
    res = res.replace('.ms','')
    res = res.replace('.','')
    print(res)
    file = open('text.txt', 'w')
    #y = "Hello World2" 
    file.write(res)
    file.close()
    #dist = distance()
    #subprocess.call(['espeak',"There is a"+ str(res) + "in front of you about" + str(int(dist/100)) + "meters" ])
    


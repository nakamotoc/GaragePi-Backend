"""

Module for interacting with GPIO

"""
import os
from typing import Union, Optional
from dotenv import load_dotenv

from time import sleep

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


try:
  OPENER_BUTTON_PIN = int(os.environ["OPENER_BUTTON"]) or None
  OPENED_SWITCH_PIN = int(os.environ["OPENED_SWITCH"]) or None
  CLOSED_SWITCH_PIN = int(os.environ["CLOSED_SWITCH"]) or None
except ValueError as e:
  print(e)
  raise(Exception("Invalid Environment Variables"))

def setup_GPIO():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(OPENER_BUTTON_PIN, GPIO.OUT, initial=1)
  GPIO.setup(OPENED_SWITCH_PIN, GPIO.IN)
  GPIO.setup(CLOSED_SWITCH_PIN, GPIO.IN)

def press_opener_button(timing:Optional[Union[float,int]] = None):
  """
  Toggles the output pin for the opener button relay for a given amount of time.
  If no time is supplied, then 1 second is used for timing.

  Args:
    timing (:obj:`Union[float,int]`, optional): The length of time to sleep in seconds. Defaults
      to one second.

  """
  if timing is None:
    timing = 1
  setup_GPIO()
  GPIO.output(OPENER_BUTTON_PIN, True)
  sleep(1)
  GPIO.output(OPENER_BUTTON_PIN, False)
  sleep(timing)
  GPIO.output(OPENER_BUTTON_PIN, True)


  
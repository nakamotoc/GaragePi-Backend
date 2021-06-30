import os
from dotenv import load_dotenv

import pytest

from app import create_app

# Load environment variables
load_dotenv()

try:
  OPENER_BUTTON_PIN = int(os.environ["OPENER_BUTTON"]) or None
  OPENED_SWITCH_PIN = int(os.environ["OPENED_SWITCH"]) or None
  CLOSED_SWITCH_PIN = int(os.environ["CLOSED_SWITCH"]) or None
except ValueError as e:
  print(e)
  raise(Exception("Invalid Environment Variables"))

import RPi.GPIO as RPiGPIO
@pytest.fixture(scope="function")
def GPIO():
  RPiGPIO.setmode(RPiGPIO.BCM)
  yield RPiGPIO
  RPiGPIO.cleanup()

@pytest.fixture(scope="session")
def OPENER_BUTTON():
  """
  The garage door remote relay "button" pin
  """
  return OPENER_BUTTON_PIN

@pytest.fixture(scope="session")
def OPENED_SWITCH():
  """
  The garage door fully opened sensor
  """
  return OPENED_SWITCH_PIN

@pytest.fixture(scope="session")
def CLOSED_SWITCH():
  """
  The garage door fully closed sensor
  """
  return CLOSED_SWITCH_PIN

@pytest.fixture(scope="session")
def app():
  """
  The Flask app
  """
  app = create_app()
  yield app
from time import sleep, time

from app.gpio import *


def test_opener_button_output(GPIO, OPENER_BUTTON):
  """
  GIVEN acces to the Raspberry Pi GPIO and an assigned opener button relay pin

  WHEN the pin is toggled high, then low, through software

  THEN the pin state is toggled high then low. If hooked up to a mechanical relay, an audible sound
  is heard during toggling.
  """
  assert OPENER_BUTTON is not None
  GPIO.setup(OPENER_BUTTON, GPIO.OUT)
  GPIO.output(OPENER_BUTTON, True)
  sleep(1)
  GPIO.output(OPENER_BUTTON, False)
  sleep(1)
  GPIO.output(OPENER_BUTTON, True)


def test_press_opener_button():
  """
  GIVEN acces to the Raspberry Pi GPIO and an assigned opener button relay pin

  WHEN the toggle function is called

  THEN the pin state is toggled from high to low and back to high. If hooked up to a mechanical relay, an audible sound
  is heard during toggling.
  """
  press_opener_button()

def test_press_opener_button_timing():
  """
  GIVEN acces to the Raspberry Pi GPIO and an assigned opener button relay pin

  WHEN the toggle function is called with timing supplied

  THEN the pin state is toggled high for 1 second, then low for the time specified, and returned high.
  """
  press_time = 2
  tolerance = 0.1
  start_time = time()
  press_opener_button(press_time)
  end_time = time()
  measured_time = end_time - start_time
  expected_time = press_time + 1
  assert abs(measured_time - expected_time) < tolerance
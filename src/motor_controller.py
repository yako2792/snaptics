import time
import RPi.GPIO as GPIO

class StepperMotorController:
    """
    A utility class to control a stepper motor using a TB6600 driver.
    """

    def __init__(self, dir_pin, step_pin, enable_pin=None):
        """
        Initialize the GPIO pins for the stepper motor.

        :param dir_pin: GPIO pin connected to the DIR input of TB6600.
        :param step_pin: GPIO pin connected to the STEP input of TB6600.
        :param enable_pin: (Optional) GPIO pin connected to the ENA input of TB6600.
        """
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        if self.enable_pin is not None:
            GPIO.setup(self.enable_pin, GPIO.OUT)
            GPIO.output(self.enable_pin, GPIO.LOW)  # Enable the driver

    def move_steps(self, steps, direction=True, delay=0.001):
        """
        Move the stepper motor a specific number of steps.

        :param steps: Number of steps to move.
        :param direction: Direction of rotation. True for one direction, False for the other.
        :param delay: Delay between steps in seconds.
        """
        GPIO.output(self.dir_pin, GPIO.HIGH if direction else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

    def cleanup(self):
        """
        Clean up GPIO settings.
        """
        GPIO.cleanup()

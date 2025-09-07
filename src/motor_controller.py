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

    def move_steps(self, steps, direction=True, delay=0.001):
        """
        Move the stepper motor a specific number of steps.

        :param steps: Number of steps to move.
        :param direction: Direction of rotation. True for one direction, False for the other.
        :param delay: Delay between steps in seconds.
        """
        self.motor_init()

        GPIO.output(self.dir_pin, GPIO.HIGH if direction else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

        self.cleanup()

    def move_degs(self, degrees, direction=True, delay=0.001):
        """
        Mueve el motor paso a paso un número específico de grados.

        :param degrees: Número de grados a mover.
        :param direction: Dirección de rotación. True para una dirección, False para la otra.
        :param delay: Retardo entre pasos en segundos.
        """
        steps_per_degree = 200 * 20 / 360  # 11.11 pasos por grado
        steps = int(degrees * steps_per_degree)
        self.move_steps(steps, direction, delay)

    def cleanup(self):
        """
        Clean up GPIO settings.
        """
        GPIO.cleanup()

    def motor_init(self) -> bool:
        try:
            print("Seteando pineas a modo board")
            GPIO.setmode(GPIO.BOARD)
            print("Seteando dir pin como GPIO out")
            GPIO.setup(self.dir_pin, GPIO.OUT)
            print("Seteando step pin como GPIO out")
            GPIO.setup(self.step_pin, GPIO.OUT)
            if self.enable_pin is not None:
                GPIO.setup(self.enable_pin, GPIO.OUT)
                GPIO.output(self.enable_pin, GPIO.LOW)  # Enable the driver
            
            return True
        
        except Exception as e:
            print(f"Setear los pines fallo con {e}")
            self.cleanup()
            return False


# motor = StepperMotorController(dir_pin=10, step_pin=8)
# # motor.move_steps(steps=2000)
# for i in range(0, 4):
#     motor.move_degs(45)
#     time.sleep(5)
# motor.cleanup()
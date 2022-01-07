import time
from threading import Thread

from gpiozero import LED

from apa102 import APA102

power = LED(5)
power.on()


class ColorManager(Thread):

    def __init__(self, color):
        super().__init__()
        self.driver = APA102(num_led=12)
        for i in range(12):
            self.driver.set_pixel(i, color[0], color[1], color[2])

    def run(self):
        self.driver.show()

    def __del__(self):
        self.driver.clear_strip()

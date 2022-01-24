
from threading import Thread

from gpiozero import LED

from apa102 import APA102

COLORS_RGB = dict(
    blue=(0, 0, 255),
    green=(0, 255, 0),
    orange=(255, 128, 0),
    pink=(255, 51, 153),
    purple=(128, 0, 128),
    red=(255, 0, 0),
    white=(255, 255, 255),
    yellow=(255, 255, 51),
    off=(0, 0, 0),
)

power = LED(5)
power.on()


class ColorManager(Thread):

    def __init__(self):
        super().__init__()
        self.driver = APA102(num_led=12)
        self.color = COLORS_RGB['red']
        for i in range(12):
            self.driver.set_pixel(i, self.color[0], self.color[1], self.color[2])

    def run(self):
        self.driver.show()

    def __del__(self):
        self.driver.clear_strip()

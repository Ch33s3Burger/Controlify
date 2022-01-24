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

    def __init__(self, color_name='red'):
        super().__init__()
        self.driver = APA102(count=12)
        self.color = COLORS_RGB[color_name]
        self.turned_on = False

    def lights_on(self):
        if self.turned_on is False:
            self.set_color(self.color[0], self.color[1], self.color[2])
            self.driver.show()
            self.turned_on = True

    def light_off(self):
        self.set_color(0, 0, 0)
        self.driver.show()
        self.turned_on = False

    def set_color(self, r, g, b):
        for i in range(12):
            self.driver.set_pixel(i, r, g, b)
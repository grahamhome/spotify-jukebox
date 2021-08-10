import pifx
import os
from random import choices, randrange


class LifxSwitch:

    def __init__(self):
        self.lights = {}
        self.lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"))

    def get_lights(self):
        lights = self.lifx_client.list_lights()
        for light in lights:
            selector = f"id:{light.get('id')}",
            if zones := light.get("zones"):
                n = len(zones)
                while n > 5:
                    inc = randrange(2, 5)


    def set_scene(self, colors):
        """
        Given a list of colors, sets each available light/zone to a random color.
        :param colors:
        :return:
        """
        print("setting scene")
        lights = self.lifx_client.list_lights()
        population, weights = zip(*colors)
        light_colors = choices(population=population, k=len(lights))
        light_settings = [
            {
                "selector": f"id:{light.get('id')}",
                "color": color,
                "power": "on",
                "brightness": float(os.environ.get("LIFX_INTENSITY", 0.5)),
                "duration": 2
            } for light, color in zip(lights, light_colors)
        ]
        self.lifx_client.set_states(light_settings)
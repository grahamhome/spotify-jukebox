from pprint import pprint

import pifx
import os
from random import choice
from concurrent.futures import ThreadPoolExecutor, as_completed


class LifxSwitch:

    def __init__(self):
        self.lights = {}

    def list_lights(self):
        lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"))
        return lifx_client.list_lights()

    def set_scene(self, colors):
        """
        Given a list of colors, sets each available light/zone to a random color.
        :param colors:
        :return:
        """
        print("setting scene")
        lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"))
        def set_lifx_state(selector, color):
            print(f"Setting {selector} to {color}")
            lifx_client.set_state(selector=selector, color=color, power="on", brightness=1, duration=2)

        lights = lifx_client.list_lights()
        light_colors = []
        for light in lights:
            # if light.get("zones"):
            #     for zone in light.get("zones").get("zones"):
            #         light_colors.append({"selector": f"id:{light.get('id')}|{zone.get('zone')}", "color": choice(colors)[1]})
            # else:
            color = choice([color for color in colors if color != self.lights.get(light.get("id"))])[1]
            light_colors.append({"selector": f"id:{light.get('id')}", "color": color,  "power": "on", "brightness": 1, "duration": 2})
            self.lights[light.get('id')] = color
        lifx_client.set_states(light_colors)
        # with ThreadPoolExecutor(max_workers=len(light_colors)+1) as pool:
        #     result_futures = {pool.submit(set_lifx_state, **light_color) for light_color in light_colors}
        #     for future in as_completed(result_futures):
        #         try:
        #             res = future.result()
        #         except Exception as exc:
        #             print(f"Light failed to update! " + str(exc))
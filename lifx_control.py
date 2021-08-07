from pprint import pprint

import pifx
import os
from random import choice
from concurrent.futures import ThreadPoolExecutor, as_completed


def list_lights():
    lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"))
    return lifx_client.list_lights()

def set_scene(colors):
    """
    Given a list of colors, sets each available light/zone to a random color.
    :param colors:
    :return:
    """
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
        light_colors.append({"selector": f"id:{light.get('id')}", "color": choice(colors)[1]})
    with ThreadPoolExecutor(max_workers=10) as pool:
        result_futures = {pool.submit(set_lifx_state, **light_color) for light_color in light_colors}
        for future in as_completed(result_futures):
            try:
                res = future.result()
            except Exception as exc:
                print(f"Light failed to update! " + str(exc))
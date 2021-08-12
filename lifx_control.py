from concurrent.futures import ThreadPoolExecutor, as_completed

import pifx
import os
from random import choices, randrange, choice


class LifxSwitch:

    num_segments = 3

    def __init__(self):
        self.bulbs = {}
        self.strips = {}
        self.lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"))
        self.get_lights(self.num_segments)
        self.pool = ThreadPoolExecutor(max_workers=10)

    def get_lights(self, num_segments):
        lights = [light for light in self.lifx_client.list_lights() if light.get("connected")]
        for light in lights:
            selector = f"id:{light.get('id')}"
            if light.get("zones"):
                num_zones = light.get("zones").get("count")
                limit = num_zones // num_segments
                sections = {}
                start_index = 0
                stop_index = 0
                while stop_index < num_zones-1:
                    stop_index = start_index+limit
                    if stop_index > num_zones-1:
                        stop_index = num_zones-1
                    sections[f"id:{light.get('id')}|{start_index}-{stop_index}"] = None
                    start_index += limit + 1

                self.strips[selector] = sections
                print(sections)
            else:
                self.bulbs[selector] = None



    def set_scene(self, colors):
        """
        Given a list of colors, sets each available light/zone to a random color.
        :param colors:
        :return:
        """
        print("setting scene")
        self.bulb_settings = []
        for bulb_id, bulb_color in self.bulbs.items():
            allowed_colors = [color for color in colors if color != bulb_color]
            self.bulbs[bulb_id] = choice(allowed_colors)

        for strip_id, strip_segments in self.strips.items():
            last_segment_color = None
            for segment_id, segment_color in strip_segments.items():
                allowed_colors = [color for color in colors if color != last_segment_color and color != segment_color]
                self.strips[strip_id][segment_id] = choice(allowed_colors)
                last_segment_color = self.strips[strip_id][segment_id]

        bulb_settings = [
            {
                "selector": bulb_selector,
                "color": bulb_color,
                "power": "on",
                "brightness": float(os.environ.get("LIFX_INTENSITY", 0.5)),
                "duration": 2
            } for bulb_selector, bulb_color in self.bulbs.items()
        ]

        for strip, strip_segments in self.strips.items():
            strip_settings = [
            {
                "selector": segment_id,
                "color": segment_color,
                "power": "on",
                "brightness": float(os.environ.get("LIFX_INTENSITY", 0.5)),
                "duration": 2
            } for segment_id, segment_color in strip_segments.items()
            ]
            bulb_settings.extend(strip_settings)

        def set_lights(states):
            self.lifx_client.set_states(states)

        futures = []
        for i in range(0, len(bulb_settings), 2):
            futures.append(self.pool.submit(set_lights, bulb_settings[i:i+2]))
        as_completed(futures)

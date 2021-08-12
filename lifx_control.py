from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

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

    def set_scene_pulse(self, color_pairs):
        """
        Given a list of color pairs and a BPM, sets available lights/zones to pulse between color pairs.
        :param color_pairs:
        :return:
        """
        print("setting pulse")
        # Set bulbs
        bulb_settings = {bulb_id: color_pairs[index] for index, bulb_id in enumerate(self.bulbs.keys())}
        # # Set segments
        # for strip_id, strip_segments in self.strips.items():
        #     for index, segment_id in enumerate(strip_segments.keys()):
        #         bulb_settings[segment_id] = color_pairs[index]

        def set_pulse(light_id, colors):
            print(f"setting {light_id} to {colors}")
            self.lifx_client.pulse_lights(selector=light_id, from_color=f"rgb:{colors[1][0]},{colors[1][1]},{colors[1][2]}",
                                            color=f"rgb:{colors[0][0]},{colors[0][1]},{colors[0][2]}", period=4, cycles=4)
            # for _ in range(20):
            #     self.lifx_client.set_states([{"selector": light_id, "color": f"rgb:{colors[1][0]},{colors[1][1]},{colors[1][2]}"}])
            #     sleep(2)
            #     self.lifx_client.set_states(
            #         [{"selector": light_id, "color": f"rgb:{colors[0][0]},{colors[0][1]}, {colors[0][2]}"}])

        outcomes = []
        print(bulb_settings.items())
        for selector, color_pair in bulb_settings.items():
            print(f"Setting {selector} to {color_pair}")
            self.pool.submit(set_pulse, kwargs={"light_id": selector, "colors": color_pair})

            outcomes.append(self.pool.submit(set_pulse, args=(selector, color_pair)))
        as_completed(outcomes)

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
                "duration": 1
            } for bulb_selector, bulb_color in self.bulbs.items()
        ]

        for strip, strip_segments in self.strips.items():
            strip_settings = [
            {
                "selector": segment_id,
                "color": segment_color,
                "power": "on",
                "brightness": float(os.environ.get("LIFX_INTENSITY", 0.5)),
                "duration": 1
            } for segment_id, segment_color in strip_segments.items()
            ]
            bulb_settings.extend(strip_settings)

        def set_lights(states):
            self.lifx_client.set_states(states)

        outcomes = []
        for i in range(0, len(bulb_settings), 2):
            outcomes.append(self.pool.submit(set_lights, bulb_settings[i:i+2]))
        as_completed(outcomes)

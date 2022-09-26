from itertools import cycle

import pifx
import os
from random import shuffle

from song import Song
import asyncio
import logging


class Lifx:
    num_segments = 3
    logger = logging.getLogger("lifx")

    def __init__(self, now_playing: Song, loop):
        self.bulbs = {}
        self.strips = {}
        self.initialized = False
        self.lifx_client = pifx.PIFX(api_key=os.environ.get("LIFX_KEY"), is_async=True, loop=loop)
        self.follow_on = True
        self.now_playing = now_playing
        self.logger.info("Lifx client created")

    async def setup(self):
        self.logger.info("Detecting lights")
        lights = [light for light in await self.lifx_client.list_lights() if light.get("connected")]
        self.logger.info(f"{len(lights)} lights found")
        for light in lights:
            selector = f"id:{light.get('id')}"
            if light.get("zones"):
                self.logger.info(
                    f"{light.get('label')} is a strip or beam with {light.get('zones').get('count')} zones"
                )
                num_zones = light.get("zones").get("count")
                limit = num_zones // self.num_segments
                sections = {}
                start_index = 0
                stop_index = 0
                while stop_index < num_zones - 1:
                    stop_index = start_index + limit
                    if stop_index > num_zones - 1:
                        stop_index = num_zones - 1
                    sections[f"id:{light.get('id')}|{start_index}-{stop_index}"] = None
                    start_index += limit + 1

                self.strips[selector] = sections
                self.logger.info(
                    f"{light.get('label')} will be divided into {self.num_segments} segments: "
                    f"{', '.join([segment for segment in sections.keys()])}"
                )

            else:
                self.bulbs[selector] = None
                self.logger.info(f"{light.get('label')} is a bulb")

        self.ids = list(self.bulbs.keys())
        self.ids.extend([segment_id for segment in self.strips.values() for segment_id in segment])
        self.initialized = True
        self.logger.info("Finished detecting lights.")

    async def set_scene(self, colors):
        """
        Given a list of colors, sets each available light/zone to a random color.
        :param colors:
        :return:
        """
        self.logger.info(f"Setting scene for {self.now_playing.title} with colors: {', '.join(colors)}")
        shuffle(colors)

        if len(self.ids) > len(colors):
            id_color_pairs = zip(self.ids, cycle(colors))
        else:
            id_color_pairs = zip(cycle(self.ids), colors)

        settings = [
            {
                "selector": selector,
                "color": color,
                "power": "on",
                "brightness": float(os.environ.get("LIFX_INTENSITY", 0.5)),
                "duration": 1,
            }
            for selector, color in id_color_pairs
        ]

        await self.lifx_client.set_states(settings)

        self.logger.info("Finished setting scene")

    async def follow(self):
        while 1:
            if (
                self.follow_on
                and self.initialized
                and self.now_playing.album_art_colors
                and not self.now_playing.paused
            ):
                self.logger.info("Setting scene")
                await self.set_scene(self.now_playing.album_art_colors)
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(1)

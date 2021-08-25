import aiohttp
from dotenv import load_dotenv
from google.cloud import vision
from itertools import combinations
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from concurrent import futures
import asyncio

class GoogleVision:
    """
    Provides "async" access to the Google Vision API via a threadpool.
    Future work will issue asynchronous, authenticated requests directly to the Google Vision API.
    :return:
    """

    def __init__(self):
        load_dotenv()
        self.pool = futures.ThreadPoolExecutor(max_workers=2)
        self.client = vision.ImageAnnotatorClient()

    async def download_image(self, image_url):
        async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    return image_data


    async def get_image_colors(self, image_url):
        """
        Returns the predominant colors in the given image.
        :param image_url:
        :return:
        """
        image = vision.Image(content=await self.download_image(image_url))

        response = await asyncio.get_event_loop().run_in_executor(self.pool, self.client.image_properties, image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        # return get_color_pairs(
        #     [
        #         (int(color.color.red), int(color.color.green), int(color.color.blue))
        #         for color in response.image_properties_annotation.dominant_colors.colors
        #     ]
        # )
        return [
            f"rgb:{int(color.color.red)},{int(color.color.green)},{int(color.color.blue)}"
            for color in response.image_properties_annotation.dominant_colors.colors if color.pixel_fraction > 0.009]


def get_color_pairs(colors):
    """
    Given a list of RGB colors, returns a list
    containing tuples of the colors with the largest delta E (visual difference)
    :param colors:
    :return:
    """
    return sorted(
        combinations(colors, 2),
        key=lambda color_pair: delta_e_cie1976(
            convert_color(color=sRGBColor(rgb_r=color_pair[0][0], rgb_g=color_pair[0][1], rgb_b=color_pair[0][2]), target_cs=LabColor),
            convert_color(color=sRGBColor(rgb_r=color_pair[1][0], rgb_g=color_pair[1][1], rgb_b=color_pair[1][2]), target_cs=LabColor)),
        reverse=True)

from google.cloud import vision

def get_image_colors(image_url):
    """
    Returns the predominant colors in the given image.
    :param image_url:
    :return:
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_url

    response = client.image_properties(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return sorted([
        [f"rgb:{int(color.color.red)},{int(color.color.green)},{int(color.color.blue)}", color.pixel_fraction]
        for color in response.image_properties_annotation.dominant_colors.colors if color.pixel_fraction > 0.009],
        key=lambda color: color[1], reverse=True)
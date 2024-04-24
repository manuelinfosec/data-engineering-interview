"""Utility module"""

import os
import re

import bs4
import requests

# Constants
CLEARBIT_URL = "https://logo.clearbit.com/"
IMAGE_FORMATS = [".jpg", ".png", ".svg"]


def append_schema(url: str, website: str):
    """
    Checks if a string contains a schema or append to it
    """
    # allowed schema
    allowed_schemas = ["http://", "https://"]

    # check if the URL starts with an allowed schema
    if not url.startswith(tuple(allowed_schemas)):
        # write the website and schema to the beginning of the URI
        url = website + url

    return url


def download_image(website: str) -> bytes:
    """
    Downloads image from a URL
    """

    logo_url = f"{CLEARBIT_URL}/{website}"

    try:
        # query ClearBit Public Logo APIs as a last resort
        response = requests.get(logo_url, stream=True, timeout=5)
        response.raise_for_status()
        return response.content
    except (
        # Used ChatGPT to determine each of these exceptions (without reading documentation)
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
    ):
        return None


def strip_illegal(url: str):
    """Strips a URL for safe use as a file name"""
    # characters not allowed in a filename
    illegal_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

    # replace illegal characters with underscores
    for char in illegal_chars:
        url = url.replace(char, "_")

    # remove trailing dots and schema
    url = url.strip(". ").replace("http___", "").replace("https___", "")

    return url


def save_image(
    image_data: bytes, file_name: str, data_folder: str = "data"
) -> str | None:
    """
    Saves the downloaded image data to `data` folder
    """
    # create `data` folder
    os.makedirs(data_folder, exist_ok=True)

    # construct file path and strip illegal characters
    filename = f"image_{strip_illegal(file_name)}.jpg"
    image_path = os.path.join(data_folder, filename)

    # save image to the file
    try:
        with open(image_path, "wb") as f:
            f.write(image_data)

        return image_path
    except OSError:
        return None


def is_image_tag(tag: bs4.element.Tag) -> bool:
    """Checks if a tag is of image-related type"""
    return tag.name == "img" or tag.name == "svg" or tag.name == "picture"


def parse_logo(website: str, source: str) -> str:
    """
    Parses HTML page source (source) and extracts the logo URL.

    Function uses an "early return" pattern to avoid executing code further
    in the case of a pattern match
    """
    soup = bs4.BeautifulSoup(source, features="html.parser")

    logo_url: str | None = None

    # 1. Check for the first class that has the string "logo" in it.
    try:
        logo_class: bs4.element.Tag = soup.find(class_=re.compile(".*logo.*"))
        if logo_class and is_image_tag(logo_class):
            logo_url = logo_class.get("src")
    except (AttributeError, TypeError):
        pass

    # 2. Check the first value that has the string "logo" in src.
    if not logo_url:
        try:
            logo_src: bs4.element.Tag = soup.find(src=re.compile(".*logo.*"))
            if logo_src and is_image_tag(logo_src):
                logo_url = logo_src.get("src")
        except (AttributeError, TypeError):
            pass

    # 3. Collect the meta property of "og:image"
    if not logo_url:
        try:
            og_image: bs4.element.Tag = soup.find("meta", property="og:image")
            if og_image:
                logo_url = og_image.get("content")
        except (AttributeError, TypeError):
            pass

    # 4. Check the first alt attribute with the string "logo" in it.
    if not logo_url:
        try:
            logo_alt: bs4.element.Tag = soup.find(attrs={"alt": re.compile(".*logo.*")})
            if logo_alt and is_image_tag(logo_alt):
                logo_url = logo_alt.get("src")
        except (AttributeError, TypeError):
            pass

    # UNUSED: 5. Collect the first .jpg, .png, .svg on the site.
    # if not logo_url:
    #     try:
    #         # Find the first <img> tag filter from IMAGE_FORMATS a match for...
    #         first_image_tag: bs4.element.Tag = soup.find(
    #             src=lambda s: any(format in s for format in IMAGE_FORMATS)
    #         )
    #         logo_url = first_image_tag["src"]
    #     except (AttributeError, TypeError):
    #        pass

    # 6. Final Resort: Query Public Logo API
    if not logo_url:
        # download and save image to local drive
        logo_bytes = download_image(website)
        logo_url = save_image(logo_bytes, website) if logo_bytes else None

    # UNUSED: Check if `logo_url` starts with schema then append the website name.
    # logo_url = append_schema(logo_url, website)

    return logo_url

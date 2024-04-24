"""Utility module"""

import os
import re
import requests

import bs4

CLEARBIT_URL = "https://logo.clearbit.com/"
IMAGE_FORMATS = [".jpg", ".png", ".svg"]


def download_image(website: str) -> bytes:
    """
    Downloads image from a URL
    """
    # Build URL string
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


def save_image(
    image_data: bytes, file_name: str, data_folder: str = "data"
) -> str | None:
    """
    Saves the downloaded image data to `data` folder
    """
    # create `data` folder
    os.makedirs(data_folder, exist_ok=True)

    # construct file path
    filename = f"image_{file_name}.jpg"
    image_path = os.path.join(data_folder, filename)

    # Save the image content to the file
    try:
        with open(image_path, "wb") as f:
            f.write(image_data)

        return image_path
    except OSError as e:
        print(f"Error saving image: {e}")
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

    # 1. Collect the meta property of "og:image"
    try:
        og_image: bs4.element.Tag = soup.find("meta", property="og:image")
        if og_image:
            print("OG Meta detected")
            logo_url = og_image.get("content")
    except (AttributeError, TypeError) as e:
        print("Error extracting og:image meta: ", e)

    # 2. Check for the first class that has the string "logo" in it.
    if not logo_url:
        try:
            logo_class: bs4.element.Tag = soup.find(class_=re.compile(".*logo.*"))
            if logo_class and is_image_tag(logo_class):
                print("Logo Class detected")
                logo_url = logo_class.get("src")
        except (AttributeError, TypeError) as e:
            print("Error extracting logo class: ", e)

    # 3. Check the first value that has the string "logo" in src.
    if not logo_url:
        try:
            logo_src: bs4.element.Tag = soup.find(src=re.compile(".*logo.*"))
            if logo_src and is_image_tag(logo_src):
                print("Logo Src Detected")
                logo_url = logo_src.get("src")
        except (AttributeError, TypeError) as e:
            print("Error extracting logo `src`: ", e)

    # 4. Check the first alt attribute with the string "logo" in it.
    if not logo_url:
        try:
            logo_alt: bs4.element.Tag = soup.find(attrs={"alt": re.compile(".*logo.*")})
            if logo_alt and is_image_tag(logo_alt):
                print("Logo Alt Detected")
                logo_url = logo_alt.get("src")
        except (AttributeError, TypeError) as e:
            print("Error extracting logo alt: ", e)

    # 5. Collect the first .jpg, .png, .svg on the site.
    if not logo_url:
        try:
            # Find the first <img> tag filter from IMAGE_FORMATS a match for...
            first_image_tag: bs4.element.Tag = soup.find(
                src=lambda s: any(format in s for format in IMAGE_FORMATS)
            )
            logo_url = first_image_tag["src"]
        except (AttributeError, TypeError) as e:
            print("Error extracting first image: ", e)

    # TODO: Check if `logo_url` starts with schema then append the website name.

    return logo_url

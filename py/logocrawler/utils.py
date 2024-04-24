"""Utility module"""

import re

import bs4

IMAGE_FORMATS = [".jpg", ".png", ".svg"]


def is_image_tag(tag):
    """Checks if a tag is of image-related type"""
    return tag.name == "img" or tag.name == "svg" or tag.name == "picture"


def parse_logo(source: str) -> str:
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

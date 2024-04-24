"""A program that will crawl a list of website and output their logo URLs."""

from typing import Optional

import requests
from scrape import download_image, parse_logo, save_image


def collect_websites() -> list[str]:
    """Collects a list of websites from STDIN."""
    print("Enter a list of websites to scrape (separated by newline):")
    websites = []
    while True:
        line = input()
        if not line:
            break
        websites.append(line.strip())
    return websites


def prepend_http(website: str) -> str:
    """Adds 'http://' to the website URL if it doesn't already start with it."""
    if not website.startswith("http"):
        website = "http://" + website
    return website


def fetch_page_source(website: str) -> Optional[str]:
    """Fetches the page source code for a given website."""
    try:
        response = requests.get(website, timeout=5)
        response.raise_for_status()  # raise an exception for non-200 status codes
        return response.text
    # handle possible network erros
    except (
        # used ChatGPT to determine each of these exceptions (without reading documentation)
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
    ):
        # TODO: Log website and error message for further probing
        return None


def main():
    """Program entry point."""
    websites = collect_websites()
    print("Starting scraping...\n")
    
    # CSV Headers
    print("website,path")

    for domain in websites:
        # add a schema to website
        website = prepend_http(domain)

        # fetch page HTML source
        page_source = fetch_page_source(website)

        # if website is unreachable for scraping, use Public Logo API
        if not page_source:
            # download and save image to local drive
            logo_bytes = download_image(website)
            logo_url = save_image(logo_bytes, website)

            # display path to local image
            print(f"{domain},{logo_url}")

            # skip to next website
            continue

        # parse page HTML and extract possible logo URL
        logo_url = parse_logo(website, page_source)

        print(f"{domain},{logo_url}")


if __name__ == "__main__":
    main()

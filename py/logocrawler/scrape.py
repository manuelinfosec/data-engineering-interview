from typing import Optional

import requests


from utils import parse_logo


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
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.text
    # Handle possible network erros
    except (
        # Used ChatGPT to determine each of these exceptions (without reading documentation)
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
    ):
        # TODO: Log website and error message for further probing
        # print(f"Error fetching page source for {website}: {e}")
        return None


def main():
    """Program entry point."""
    websites = collect_websites()

    # TODO: CSV Headers
    print("Starting scraping...\n")
    for website in websites:
        print(f"Website: {website}")
        website = prepend_http(website)

        page_source = fetch_page_source(website)
        if page_source is None:
            print(f"Not Reachable: {website}")
            continue

        logo_url = parse_logo(page_source)
        print("******************************************************************")
        print(logo_url)


if __name__ == "__main__":
    main()

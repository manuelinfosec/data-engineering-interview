"""Tests for logo crawler"""

import requests
from scrape import parse_logo, strip_illegal


def test_parse_logo():
    """Tests the `parse_logo` function"""

    # send request and extrat page source
    response = requests.get("https://www.facebook.com", timeout=5)
    page_source = response.text

    logo_url = parse_logo("https://www.facebook.com", page_source)

    expected_logo_url = "https://static.xx.fbcdn.net/rsrc.php/y1/r/4lCu2zih0ca.svg"

    # assert that the returned logo URL matches our expected URL
    assert logo_url == expected_logo_url


def test_strip_illegal():
    """Test the `strip_illegal` function"""
    # test with various URLs containing illegal characters
    assert strip_illegal("https://twitter.com") == "twitter.com"
    assert strip_illegal("http://twitter.com") == "twitter.com"
    assert strip_illegal("https://twitter.com/?q=test") == "twitter.com__q=test"
    assert (
        strip_illegal("https://twitter.com/path/to/file.jpg")
        == "twitter.com_path_to_file.jpg"
    )
    assert strip_illegal("https://twitter.com:8080") == "twitter.com_8080"
    assert (
        strip_illegal("https://twitter.com/<script>alert('Hello')</script>")
        == "twitter.com__script_alert('Hello')__script_"
    )
    assert strip_illegal('https://twitter.com/<>:"/\\|?*') == "twitter.com__________"

    # test with URLs already stripped
    assert strip_illegal("twitter.com") == "twitter.com"
    assert (
        strip_illegal("twitter.com_path_to_file.jpg") == "twitter.com_path_to_file.jpg"
    )

    # test with empty URL
    assert strip_illegal("") == ""

import re
import subprocess
from playwright.sync_api import sync_playwright


def get_last_login():
    result = subprocess.run(
        ["last", "-3", "--time-format", "iso", "joshnelson"],
        capture_output=True,
        text=True
    )
    third_entry = result.stdout.splitlines()[2]
    timestamps = re.findall(
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
        third_entry
    )
    logout_timestamp = timestamps[1]
    date, time = logout_timestamp.split("T")
    time = time[:5]  # HH:MM
    return (date, time)


def take_screenshot(url: str, output_path: str = "screenshot.jpeg") -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.screenshot(path=output_path)
        browser.close()
    return output_path


last_login = get_last_login()
print(last_login)

filename = take_screenshot("https://google.com")
print(filename)
import os
import re
import subprocess
import time
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


def take_screenshot(url: str, output_path: str = "screenshot.png") -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.screenshot(path=output_path)
        browser.close()
    return output_path


def set_wallpaper(image_path: str):
    abs_path = os.path.abspath(image_path)
    script = f"""
    var allDesktops = desktops();
    for (var i = 0; i < allDesktops.length; i++) {{
        var d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
        d.writeConfig("Image", "file://{abs_path}");
    }}
    """
    result = subprocess.run(
        ["qdbus6", "org.kde.plasmashell", "/PlasmaShell",
         "org.kde.PlasmaShell.evaluateScript", script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error setting wallpaper: {result.stderr}")
    else:
        print(f"Wallpaper set to: {abs_path}")

last_login = get_last_login()
print(last_login)

filename = take_screenshot("https://google.com")
print(filename)

set_wallpaper(filename)
time.sleep(5)
# Call this whenever you want your wallpaper back:
SWEET_WALLPAPER = "/home/joshnelson/.local/share/wallpapers/Sweet-Wallpapers/Sweet-space.png"
set_wallpaper(SWEET_WALLPAPER)
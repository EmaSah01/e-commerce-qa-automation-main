import os
from datetime import datetime


def save_screenshot(driver, name_prefix: str = "shot", folder: str = "reports/screenshots"):
    os.makedirs(folder, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = os.path.join(folder, f"{name_prefix}-{ts}.png")
    driver.save_screenshot(path)
    return path

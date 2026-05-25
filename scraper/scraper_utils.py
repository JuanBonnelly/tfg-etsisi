import os

import undetected_chromedriver as uc

PROFILE_DIR = os.path.join(os.path.expanduser("~"), "fbref_profile") 

def make_driver(headless: bool = False):
    opts = uc.ChromeOptions()
    
    opts.add_argument(f"--user-data-dir={PROFILE_DIR}")
    opts.add_argument("--profile-directory=Default")

    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument("--lang=en-US,en;q=0.9")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1280,900")

    driver = uc.Chrome(options=opts, version_main=148)
    driver.set_page_load_timeout(60)
    return driver

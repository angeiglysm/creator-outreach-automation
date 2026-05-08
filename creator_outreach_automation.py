import random
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


CHROME_PROFILE = "Profile 2"
CHROME_USER_DATA_PATH = r"C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data"
CHROME_DRIVER_PATH = r"C:\Users\YOUR_USER\chromedriver.exe"

BACKSTAGE_URL = "https://live-backstage.tiktok.com/portal/anchor/instant-messages"

PROFILES_FILE = "profiles.txt"
CONTACTED_FILE = "contacted_profiles.txt"

MAX_PROFILES = 200

MESSAGE_TEMPLATES = [
    "Hello! We noticed your profile and think you could be a great fit for our creator program. If you're interested, I can share more details.",
    "Hi! Your content has great potential. We would love to share information about our creator partnership program if you're interested."
]


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_PATH}")
    chrome_options.add_argument(f"--profile-directory={CHROME_PROFILE}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(2)
    driver.maximize_window()

    return driver


def load_profiles(file_path):
    path = Path(file_path)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def save_contacted_profiles(profiles):
    with open(CONTACTED_FILE, "a", encoding="utf-8") as file:
        for profile in profiles:
            file.write(f"{profile}\n")


def send_outreach_messages(profiles):
    driver = create_driver()
    contacted_profiles = []

    try:
        driver.get(BACKSTAGE_URL)

        for index, profile in enumerate(profiles):

            if index >= MAX_PROFILES:
                break

            try:
                search_input = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div/input")
                    )
                )

                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.BACKSPACE)
                search_input.send_keys(profile)
                search_input.send_keys(Keys.ENTER)

                sleep(3)

                first_result = driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div"
                )
                first_result.click()

                sleep(3)

                message_box = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/textarea")
                    )
                )

                previous_message_selector = (
                    "#neo-layout-fmp > div > div > div > div > div > "
                    "div.rightContainer_633b1 > div.contentArea_633b1 > "
                    "div.centerArea_633b1 > div.messageArea_633b1 > div > "
                    "div > div:nth-child(1) > div > div.messageLayout_506c9"
                )

                previous_messages = driver.find_elements(By.CSS_SELECTOR, previous_message_selector)

                if not previous_messages:
                    message = random.choice(MESSAGE_TEMPLATES)
                    message_box.send_keys(message)

                    send_button = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/button")
                        )
                    )

                    send_button.click()
                    contacted_profiles.append(profile)

                    sleep(random.randint(4, 8))

            except Exception as error:
                print(f"Could not contact {profile}: {error}")
                continue

    finally:
        driver.quit()

    save_contacted_profiles(contacted_profiles)
    print(f"Profiles contacted: {len(contacted_profiles)}")


if _name_ == "_main_":
    profiles = load_profiles(PROFILES_FILE)
    contacted = load_profiles(CONTACTED_FILE)

    pending_profiles = [
        profile for profile in profiles
        if profile not in contacted
    ]

    send_outreach_messages(pending_profiles)
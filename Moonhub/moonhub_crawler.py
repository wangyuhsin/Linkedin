import sys
import time
import csv

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def search_scrape():
    # Configure Chrome to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Open the Moonhub chat page
    driver.get("https://chat.moonhub.ai/")
    time.sleep(3)

    # Input email address
    email = input("Please enter your email: ")
    username = driver.find_element(By.ID, "username")
    username.send_keys(email)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Input verification code
    code = input("Please enter your verification code: ")
    pword = driver.find_element(By.ID, "code")
    pword.send_keys(code)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Specify the number of pages to retrieve
    page_num = input("How many pages of information do you want to retrieve? ")
    time.sleep(5)

    print("Scraping...")

    # Expand the list to load more profiles
    buttons = driver.find_elements(By.XPATH, "//*[@id='expand-button']")
    last_button = buttons[-1]
    last_button.click()

    profile_links = []

    for i in tqdm(range(int(page_num))):
        time.sleep(5)

        # Click the "View Full Profile" button
        driver.find_elements(By.XPATH, "//*[@id='view-full-profile-button']")[0].click()
        time.sleep(5)

        for j in range(25):
            # Click a button to reveal LinkedIn profile URL
            driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
            )[6].click()

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            profile_url = driver.current_url

            # Extract the LinkedIn profile URL
            if not profile_url.startswith("https://www.linkedin.com/checkpoint/"):
                if "sessionRedirect" in profile_url:
                    profile_links.append(
                        [
                            profile_url.split("sessionRedirect=")[1]
                            .replace("%3A", ":")
                            .replace("%2F", "/")
                            .split("%")[0]
                        ]
                    )
                else:
                    profile_links.append([profile_url.split("?original_referer=")[0]])

            # Close the new tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Click the next button to reveal more profiles
            driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
            )[4].click()

        # Close the current tab
        driver.find_elements(
            By.CSS_SELECTOR,
            "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
        )[5].click()

        # Click the next page button to load more profiles
        driver.find_elements(
            By.CSS_SELECTOR,
            "button.MuiButtonBase-root.MuiPaginationItem-circular.MuiPaginationItem-previousNext.MuiPaginationItem-root.MuiPaginationItem-sizeSmall.MuiPaginationItem-text.MuiPaginationItem-textPrimary.css-3ta4e3[aria-label='Go to next page'][tabindex='0'][type='button']",
        )[0].click()

    driver.quit()

    return profile_links


def to_csv(file_name, profile_links):
    # Write a list of profile links to a CSV file
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(profile_links)


if __name__ == "__main__":
    file_name = "moonhub_list.csv"
    profile_links = search_scrape()

    if profile_links:
        to_csv(file_name, profile_links)
        print(
            f"{len(profile_links)} profile links have been successfully saved to {file_name}."
        )
    else:
        print("No profile links were scraped.")

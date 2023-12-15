import sys
import time
import csv

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
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
        try:
            view_profile = driver.find_elements(
                By.XPATH, "//*[@id='view-full-profile-button']"
            )
            view_profile[0].click()
        except ElementClickInterceptedException:
            print(
                "ElementClickInterceptedException: Click intercepted, breaking the loop."
            )
            break

        for j in range(25):
            try:
                condition = 0
                time.sleep(1)
                # Click a button to reveal LinkedIn profile URL
                driver.find_elements(
                    By.CSS_SELECTOR,
                    "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                )[-1].click()

                # Switch to the new tab
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                else:
                    continue
                time.sleep(2)
                profile_url = driver.current_url

                if profile_url.startswith("https://github.com/"):
                    condition = 1
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                    )[-2].click()
                    # Switch to the new tab
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[1])
                    else:
                        continue
                    time.sleep(2)
                    profile_url = driver.current_url

                # Extract the LinkedIn profile URL
                if not profile_url.startswith("https://www.linkedin.com/checkpoint/"):
                    if "sessionRedirect" in profile_url:
                        link = (
                            profile_url.split("sessionRedirect=")[1]
                            .replace("%3A", ":")
                            .replace("%2F", "/")
                            .split("%")[0]
                        )
                        if link != "https://www.linkedin.com/in/":
                            profile_links.append([link])
                    else:
                        link = profile_url.split("?original_referer=")[0]
                        if link != "https://www.linkedin.com/in/":
                            profile_links.append([link])

                # Close the new tab and switch back to the main tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Click the next button to reveal more profiles
                if condition == 0:
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                    )[-3].click()
                else:
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                    )[-4].click()
            except WebDriverException as e:
                print(f"Error encountered: {e}. Skipping to the next profile.")
                driver.switch_to.window(driver.window_handles[0])
                # Click the next button to reveal more profiles
                if condition == 0:
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                    )[-3].click()
                else:
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
                    )[-4].click()
                continue

        # Close the current tab
        if condition == 0:
            driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
            )[-2].click()
        else:
            driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1a4yhh1[tabindex='0'][type='button']",
            )[-3].click()

        time.sleep(2)

        # Click the next page button to load more profiles
        if i < 2:
            next_page = driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiPaginationItem-circular.MuiPaginationItem-previousNext.MuiPaginationItem-root.MuiPaginationItem-sizeSmall.MuiPaginationItem-text.MuiPaginationItem-textPrimary.css-3ta4e3[aria-label='Go to next page'][tabindex='0'][type='button']",
            )
        else:
            next_page = driver.find_elements(
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiPaginationItem-root.MuiPaginationItem-sizeSmall.MuiPaginationItem-text.MuiPaginationItem-circular.MuiPaginationItem-textPrimary.MuiPaginationItem-previousNext.css-3ta4e3[aria-label='Go to next page'][tabindex='0'][type='button']",
            )
        if next_page != []:
            next_page[0].click()
        else:
            break

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

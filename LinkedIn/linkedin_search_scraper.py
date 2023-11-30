# Import necessary libraries
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from constants import *


def search_scrape():
    """
    Scrape LinkedIn search results for profile links.

    This function performs the following steps:
    1. Configures Chrome to run in headless mode for automated browsing.
    2. Navigates to the LinkedIn login page and logs in using provided credentials.
    3. Navigates to the LinkedIn search results page.
    4. Scrapes profile links from the search results.
    5. Continues scrolling and collecting profile links until reaching SCRAPE_NUM.

    Returns:
    - profile_links (list): List of profile links scraped from LinkedIn search results.
    """
    # We can only extract maximum 1000 LinkedIn search results per day
    if SCRAPE_NUM > 1000:
        print(
            "Please set SCRAPE_NUM in constants.py to a value less than 1000."
        )
        return None

    # Configure Chrome to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the Chrome web driver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the LinkedIn login page
    driver.get("https://linkedin.com/uas/login")
    time.sleep(3)

    # Find the username and password input fields, and enter your credentials
    username = driver.find_element(By.ID, "username")
    username.send_keys(EMAIL)

    pword = driver.find_element(By.ID, "password")
    pword.send_keys(PWORD)

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Navigate to the LinkedIn search results page
    driver.get(SEARCH_URL)
    time.sleep(5)

    # Get the page source and parse it with BeautifulSoup
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")

    search_limit = int(
        soup.find("h2", {"class": "pb2 t-black--light t-14"})
        .find("div")
        .get_text(strip=True)
        .split(" ")[1]
        .replace(",", "")
    )

    if SCRAPE_NUM > search_limit:
        print(
            f"Only {search_limit} results are available. Please reduce the value of SCRAPE_NUM in constants.py"
        )
        driver.quit()
        return None

    print("Scraping profile links...")

    # Initialize a list to store profile links
    profile_links = []

    # Loop through profile items on the page and extract links
    for item in soup.findAll("div", {"class": "entity-result__item"}):
        link = (
            item.find("div", {"class": "mb1"})
            .find("a", {"class": "app-aware-link"})["href"]
            .split("?")[0]
            + "/"
        )
        action = item.find(
            "div", {"class": "entity-result__actions entity-result__divider"}
        ).find("button")["aria-label"]
        if action != "Message ":
            profile_links.append([link])

    # Continue scrolling and collecting profile links until reaching the SCRAPE_NUM
    while len(profile_links) < SCRAPE_NUM:
        initialScroll, finalScroll = 0, 1500
        driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")

        time.sleep(5)

        # Click the "Next" button to load more search results
        driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
        time.sleep(5)

        # Get the page source of the new page and parse it
        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        # Loop through profile items and extract links
        for item in soup.findAll("div", {"class": "entity-result__item"}):
            link = (
                item.find("div", {"class": "mb1"})
                .find("a", {"class": "app-aware-link"})["href"]
                .split("?")[0]
                + "/"
            )
            action = item.find(
                "div", {"class": "entity-result__actions entity-result__divider"}
            ).find("button")["aria-label"]
            if action != "Message ":
                if len(profile_links) >= SCRAPE_NUM:
                    break
                profile_links.append([link])

    # Quit the web driver when done
    driver.quit()

    return profile_links


def to_csv(file_name, profile_links):
    """
    Write a list of profile links to a CSV file.

    Args:
    - file_name (str): The name of the CSV file.
    - profile_links (list): List of profile links to be written to the CSV file.
    """
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(profile_links)


if __name__ == "__main__":
    file_name = "profile_lists.csv"
    # Call the 'search_scrape' function to retrieve profile links
    profile_links = search_scrape()
    if profile_links:
        # Write the profile links to a CSV file
        to_csv(file_name, profile_links)
        print(
            f"{SCRAPE_NUM} profile links have been successfully saved to {file_name}."
        )
    else:
        print("No profile links were scraped.")

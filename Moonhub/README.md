# Moonhub Profile Scraper

This project is designed to scrape Moonhub profiles using Selenium and BeautifulSoup, and then export the scraped data to a Google Spreadsheet.

## Files in This Repository

1. **constants.py** - This file contains the constants used across the project. It includes LinkedIn cookies (`LI_AT`, `JSESSIONID`) required for authentication and the URL of the Google Spreadsheet where the scraped data is stored. Follow the instructions [here](https://help.delpha.io/s/article/How-to-access-your-LinkedIn-Cookie) to obtain your LinkedIn cookies.

2. **requirements.txt** - A list of Python libraries required for this project. These dependencies include `beautifulsoup4`, `selenium`, and `tqdm`.

3. **moonhub_crawler.py** - The main script to be run on a local machine. It uses Selenium and BeautifulSoup to scrape LinkedIn profile links from the Moonhub chat page. The script prompts for user input to authenticate and specify the number of pages to scrape. Scraped data is saved to `moonhub_list.csv`.

4. **moonhub_to_spreadsheet.py** - This script should be run on [Naas cloud](https://app.naas.ai/user-redirect/naas/downloader?url=https://raw.githubusercontent.com/jupyter-naas/awesome-notebooks/master/LinkedIn/LinkedIn_Send_invitation_to_profile.ipynb). It reads the `moonhub_list.csv` file, processes the LinkedIn URLs, and extracts relevant information using the LinkedIn and Google Sheets APIs provided by Naas.ai. The extracted data is then uploaded to the specified Google Spreadsheet.

## Setup

Before running the scripts, you need to set up your environment and update the necessary configurations.

### Step 1: Clone the Repository

Clone this repository to your local machine using Git:

```bash
$ git clone https://github.com/wangyuhsin/Linkedin/tree/main/Moonhub
$ cd Linkedin/Moonhub
```

### Step 2: Install Dependencies

Install the required Python libraries specified in requirements.txt:

```python
$ pip install -r requirements.txt
```
This will install libraries like `beautifulsoup4`, `selenium`, and `tqdm`, which are essential for the project.

### Step 3: Update Constants

Open the `constants.py` file and replace the placeholder values with your actual LinkedIn cookies and Google Spreadsheet details:

```python
# LinkedIn cookies
LI_AT = "Your LinkedIn li_at Cookie"
JSESSIONID = "Your LinkedIn JSESSIONID Cookie"

# Google Spreadsheet details
SPREADSHEET_URL = "Your Google Spreadsheet URL"
SHEET_NAME = "Your Google Spreadsheet Sheet Name"
```
For a more detailed guide to obtaining LinkedIn cookies, refer to [this article](https://help.delpha.io/s/article/How-to-access-your-LinkedIn-Cookie).

### Step 4: Setting Up Naas

Since `moonhub_to_spreadsheet.py` is intended to be run on Naas cloud:

1. Sign up or log in to [Naas](https://naas.ai/).
2. Upload the `moonhub_to_spreadsheet.py`, `constants.py`, and the generated `moonhub_list.csv` file.
3. Run the script `moonhub_to_spreadsheet.py` in the [Naas environment](https://app.naas.ai/user-redirect/naas/downloader?url=https://raw.githubusercontent.com/jupyter-naas/awesome-notebooks/master/LinkedIn/LinkedIn_Send_invitation_to_profile.ipynb).

After completing these steps, your environment should be ready, and you can proceed with executing the scripts.

## Executing the Scripts

Once you have completed the setup, you can proceed to run the scripts. This project consists of two main scripts: `moonhub_crawler.py` for scraping LinkedIn profiles from Moonhub and `moonhub_to_spreadsheet.py` for transferring the data to a Google Spreadsheet.

### Running `moonhub_crawler.py`

This script should be run on your local machine. It will scrape LinkedIn profiles from <b>your last search</b> on Moonhub and save the data to a CSV file.

#### Important Note on Locating the LinkedIn Button

Since Moonhub does not have an ID for each button and it has a different number of buttons for every search result, we can only find the button order manually by inspecting its HTML file. There is a tutorial on how to do this in the [Demo Video](#demo-video). After finding the order, remember to change the value of `LINKEDIN_BUTTON` in `moonhub_crawler.py` accordingly.

<img width="718" alt="截圖 2023-12-13 上午1 13 52" src="https://github.com/wangyuhsin/Linkedin/assets/76431031/0648f9b3-5743-466b-a289-1ed76754f206">

After changing the value, you can execute the script:

 ```python
 $ python3 moonhub_crawler.py
 ```
The script will prompt you for your email address, verification code, and the number of pages you want to scrape. Follow the prompts to proceed.

<img width="563" alt="截圖 2023-12-12 下午5 13 50" src="https://github.com/wangyuhsin/Linkedin/assets/76431031/4da18512-fc4c-4d0c-ac28-416eb617df22">

Once the script completes, it will generate a file named `moonhub_list.csv` in the project directory containing the scraped LinkedIn profile links.

### Running `moonhub_to_spreadsheet.py`

After generating the `moonhub_list.csv` file, you can run this script to process and upload the data to a Google Spreadsheet. This script is designed to be run on the [Naas cloud platform](https://app.naas.ai/user-redirect/naas/downloader?url=https://raw.githubusercontent.com/jupyter-naas/awesome-notebooks/master/LinkedIn/LinkedIn_Send_invitation_to_profile.ipynb).

Remember to upload the `moonhub_list.csv` file and `moonhub_to_spreadsheet.py` script to Naas, and check the variables in `constants.py` before running it.

```bash
$ python3 moonhub_to_spreadsheet.py
```
<img width="1440" alt="截圖 2023-12-12 下午6 15 16" src="https://github.com/wangyuhsin/Linkedin/assets/76431031/eef56c90-dbe2-4dcf-ace0-e42375b14541">

The script will read the `moonhub_list.csv` file, connect with LinkedIn APIs to extract information from each LinkedIn profile, and update the specified Google Spreadsheet with the data.

<img width="1440" alt="截圖 2023-12-12 下午6 17 51" src="https://github.com/wangyuhsin/Linkedin/assets/76431031/70e2686f-9817-4845-9112-475d803ac11a">

By following these steps, you should be able to successfully execute the scripts and automate the process of scraping profiles from Moonhub and updating a Google Spreadsheet with the data.

### Demo Video
[<img width="1072" alt="截圖 2023-12-12 下午7 48 20" src="https://github.com/wangyuhsin/Linkedin/assets/76431031/2f8454f1-bd04-4a9c-8db6-e0851c59f849">](https://youtu.be/SWCqzP-892I)

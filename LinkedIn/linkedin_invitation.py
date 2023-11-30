import csv
import time
from datetime import date

import pandas as pd
from naas_drivers import linkedin
import naas

from constants import *

# Connect to LinkedIn using your credentials
CONNECT = linkedin.connect(LI_AT, JSESSIONID)


def replace_present_with_date(cell_value):
    """
    Replace 'Present' with the current date in YYYY-MM-DD format.

    Args:
    - cell_value (str): The value in the cell.

    Returns:
    - str: The original cell value or the current date if it was 'Present'.
    """
    if cell_value == "Present":
        return str(date.today())
    return cell_value


def filter_profiles(file_name):
    """
    Filter LinkedIn profiles based on criteria such as years of experience and education.

    Args:
    - file_name (str): The name of the CSV file containing LinkedIn profile links.

    Returns:
    - profile_links (set): Set of qualified LinkedIn profile links.
    - df (pd.DataFrame): DataFrame containing profile information of qualified profiles.
    """
    file = open(file_name, "r")
    links = list(csv.reader(file, delimiter=","))
    file.close()
    links = [item for row in links for item in row]

    profile_links = set()
    df = pd.DataFrame()

    for link in links:
        info = CONNECT.profile.get_identity(link)
        info["PROFILE_URL"] = link
        resume = CONNECT.profile.get_resume(link)

        recent_company = resume["PLACE"][0]

        yoe_df = resume[resume["CATEGORY"] == "Experience"]
        yoe_df["DATE_END"] = yoe_df["DATE_END"].apply(replace_present_with_date)
        yoe_df["DATE_START"] = pd.to_datetime(
            yoe_df["DATE_START"], format="%Y-%m", errors="coerce"
        )
        yoe_df["DATE_END"] = pd.to_datetime(
            yoe_df["DATE_END"], format="%Y-%m", errors="coerce"
        )
        yoe_df["MONTHS"] = yoe_df.apply(
            lambda row: (row["DATE_END"] - row["DATE_START"]).days // 30
            if row["DATE_END"] != pd.Timestamp("NaT")
            else None,
            axis=1,
        )
        yoe = yoe_df["MONTHS"].sum() // 12

        education = set(resume[resume["CATEGORY"] == "Education"]["PLACE"])

        if yoe >= 5 and len(education.intersection(TARGET_SCHOOLS)) != 0:
            profile_links.add(link)
            df = pd.concat([df, info], axis=0)

    df = df.reset_index()

    print(f"📋 There are {len(df)} qualified profiles.")

    return (
        profile_links,
        df[
            [
                "PROFILE_URL",
                "FIRSTNAME",
                "LASTNAME",
                "SUMMARY",
                "OCCUPATION",
                "REGION",
                "COUNTRY",
            ]
        ],
    )


def send_invitation(profile_links, message):
    """
    Send LinkedIn connection invitations to qualified profiles.

    Args:
    - profile_links (set): Set of qualified LinkedIn profile links.
    - message (str): The message to include in the invitations.
    """
    profile_links = list(set(profile_links))
    if len(profile_links) > 20:
        print("❌ You can only send up to 20 invitations per working day.")
        return
    for recipient in profile_links:
        recipient_df = CONNECT.profile.get_identity(recipient)
        first_name = recipient_df["FIRSTNAME"][0].strip().split(" ")[0]
        greeting_message = f"Hello {first_name}, \n" + message
        result = linkedin.invitation.send(
            recipient_url=recipient, message=greeting_message
        )
        print(
            result.replace("!", "to ").replace("✉️", "📮")
            + f"{first_name} ({recipient})"
        )
        if recipient != profile_links[-1]:
            time.sleep(60)


def new_connections_today():
    """
    Retrieve and print new LinkedIn connections made today.

    Returns:
    - df (pd.DataFrame): DataFrame containing information about new connections made today.
    """
    df = CONNECT.network.get_connections(limit=100)
    df["CREATED_AT"] = pd.to_datetime(df["CREATED_AT"]).dt.date
    df = df[df["CREATED_AT"] == date.today()]
    print("✅ New connections today:", len(df))
    return df[
        [
            "FIRSTNAME",
            "LASTNAME",
            "OCCUPATION",
            "CREATED_AT",
            "PROFILE_URL",
            "DATE_EXTRACT",
        ]
    ]

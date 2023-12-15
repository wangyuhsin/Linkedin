import csv
import time
from datetime import datetime
import requests

from tqdm import tqdm
import pandas as pd
from naas_drivers import linkedin, gsheet
import naas

from constants import *  # You might have constants defined in a separate file

# Function to convert CSV file to a DataFrame
def csv_to_df(file_name):
    # Read the CSV file and extract LinkedIn profile links
    file = open(file_name, "r")
    links = list(csv.reader(file, delimiter=","))
    file.close()
    links = [item for row in links for item in row]

    # Define DataFrame columns
    columns = [
        "Name",
        "LinkedIn",
        "Current Role",
        "Location",
        "Company",
        "Title",
        "Start Date",
        "End Date",
        "Current",
        "University",
        "Degree",
        "Field",
    ]
    moonhub_df = pd.DataFrame(columns=columns)
    df_gsheet = gsheet.connect(SPREADSHEET_URL).get(sheet_name=SHEET_NAME)
    if len(df_gsheet) != 0:
        exist = set(df_gsheet["LinkedIn"])
    else:
        exist = set()

    # Loop through LinkedIn profile links and extract data
    for i in tqdm(range(len(links))):
        if links[i] not in exist:
            try:
                resume_df = linkedin.connect(LI_AT, JSESSIONID).profile.get_resume(
                    links[i]
                )
                identity_df = linkedin.connect(LI_AT, JSESSIONID).profile.get_identity(
                    links[i]
                )

                # Extract various fields from the data
                full_name = resume_df["FULL_NAME"][0]
                Linkedin = links[i]
                location = identity_df["REGION"][0]
                if len(resume_df[resume_df["CATEGORY"] == "Experience"]) != 0:
                    current_role = resume_df[
                        resume_df["CATEGORY"] == "Experience"
                    ].iloc[0]["TITLE"]
                    company = resume_df[resume_df["CATEGORY"] == "Experience"].iloc[0][
                        "PLACE"
                    ]
                    title = resume_df[resume_df["CATEGORY"] == "Experience"].iloc[0][
                        "TITLE"
                    ]
                    start_date = resume_df[resume_df["CATEGORY"] == "Experience"].iloc[
                        0
                    ]["DATE_START"]
                    if start_date is not None:
                        if start_date.endswith("00"):
                            start_date = start_date.split("-")[0]
                        else:
                            start_date = str(
                                datetime.strptime(start_date, "%Y-%m").strftime("%b %Y")
                            )
                    else:
                        start_date = None
                    end_date = resume_df[resume_df["CATEGORY"] == "Experience"].iloc[0][
                        "DATE_END"
                    ]
                    if end_date is not None:
                        if end_date.endswith("00"):
                            end_date = end_date.split("-")[0]
                        else:
                            if end_date != "Present":
                                end_date = str(
                                    datetime.strptime(end_date, "%Y-%m").strftime(
                                        "%b %Y"
                                    )
                                )
                                current = "FALSE"
                            else:
                                current = "TRUE"
                    else:
                        end_date = None
                        current = None
                else:
                    current_role = None
                    company = None
                    title = None
                    start_date = None
                    end_date = None
                    current = None

                if len(resume_df[resume_df["CATEGORY"] == "Education"]) != 0:
                    university = resume_df[resume_df["CATEGORY"] == "Education"].iloc[
                        0
                    ]["PLACE"]
                    degree = resume_df[resume_df["CATEGORY"] == "Education"].iloc[0][
                        "TITLE"
                    ]
                    field = resume_df[resume_df["CATEGORY"] == "Education"].iloc[0][
                        "FIELD"
                    ]
                else:
                    university = None
                    degree = None
                    field = None

            except requests.exceptions.HTTPError as e:
                print(f"Not Found for url: {links[i]}. Continue...")
                continue

            # Append the extracted data to the DataFrame
            moonhub_df.loc[len(moonhub_df.index)] = [
                full_name,
                Linkedin,
                current_role,
                location,
                company,
                title,
                start_date,
                end_date,
                current,
                university,
                degree,
                field,
            ]
    return moonhub_df


# Function to update a Google Sheets spreadsheet with DataFrame data
def df_to_spreadsheet(df, spreadsheet_url, sheet_name):
    # Connect to the Google Sheets spreadsheet
    df_gsheet = gsheet.connect(spreadsheet_url).get(sheet_name=sheet_name)

    # Concatenate the existing data with the new data and remove duplicates
    moonhub_df = pd.concat([df_gsheet, df]).drop_duplicates("LinkedIn", keep="first")

    # Send the updated data to the Google Sheets spreadsheet
    gsheet.connect(spreadsheet_url).send(
        moonhub_df, sheet_name=sheet_name, append=False
    )
    print(f"Profiles already added to the spreadsheet: {spreadsheet_url}")


if __name__ == "__main__":
    file_name = "moonhub_list.csv"

    # Convert CSV data to a DataFrame
    df = csv_to_df(file_name)

    # Update the Google Sheets spreadsheet with the DataFrame data
    df_to_spreadsheet(df, SPREADSHEET_URL, SHEET_NAME)

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from lib.scrapper import scrape
from gspread_dataframe import set_with_dataframe
import os
import json


def main():
  creds_json = os.getenv("GOOGLE_CREDS")
  if creds_json is None:
    raise ValueError("Environment Variable GOOGLE_CREDS is not set.")
  creds_json = json.loads(creds_json)

  creds = ServiceAccountCredentials.from_json_keyfile_name("scrape_into_sheets/google-credentials.json")
  client = gspread.authorize(creds)

  sheet = client.open('scrapped-jobs-listings').sheet1

  existing_data = sheet.get_all_records(head=2)
  df_existing = pd.DataFrame(existing_data)

  data = scrape(
      type="internships",
      role=[
          "backend-development", 
          "front-end-development", 
          "full-stack-development", 
          "software-development", 
          "web-development"
      ],
      # role=["science"],
      location="delhi",
      stipend="",
      post_time=["Just now", "Today", "Few hours ago"]
  )  
  df_new = pd.DataFrame(data)
  df_new = df_new.drop(columns=["id"])

  counter_cell = sheet.acell("A1").value
  if not counter_cell:
    day_counter = 0
  else:
    day_counter = int(counter_cell)

  if day_counter >= 3:
    sheet.clear()
    set_with_dataframe(sheet, df_new, row=2)
    sheet.update([["1"]], "A1")
  else:
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(keep="first")
    sheet.clear()
    set_with_dataframe(sheet, df_combined, row=2)
    sheet.update([[str(day_counter + 1)]], "A1")
  print("Successfully updated the sheet.")


if __name__ == "__main__":
  main()
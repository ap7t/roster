import re
import io
from shift import Shift
from datetime import date
import datetime
from googleapiclient.discovery import build
import time
from auth import Auth
from ocr import OCR
import config


FILENAME = "./roster.txt"
CALENDER_ID = config.CALENDER_ID
NAME = "A PURCELL"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def read_shifts(filename):
    shifts = []
    date_pattern = r"\d{2}/\d{2}/\d{2}"
    shift_pattern = r"(\d{2}(:|.)\d{2}/\d{2}(:|.)\d{2}|FREE)"
    date = shift = None
    with open(filename, "r") as f:
        for line in f:
            if re.search(date_pattern, line):
                date = line.strip("\n")
            elif re.search(shift_pattern, line):
                line = line.split()[0]
                if ":" in line:     # sometimes times are mistyped as HH:MM not HH.MM
                    line.replace(":", ".")
                shift = line.split("/") if line != "FREE" else line
            elif re.search(f"^{NAME}", line):
                if shift != "FREE":
                    shifts.append(Shift(date, shift))
                else:
                    shifts.append(Shift(date))
                
    return shifts

def calc_total_hours(shifts):
    total = 0
    for shift in shifts[:-1]: # don"t include last shift as work week starts on Sunday
        total += shift.calculate_hours()

    return total

def upload_roster(service, shifts):
    event_ids = []
    print("Uploading roster to Google Calendar")
    for shift in shifts:
        event = {
            "summary": shift.summary,
            "colorId": shift.colour,   
        }
        if shift.all_day:
            event["start"] = {
                    "date": shift.get_start(),
                    "timeZone": "Europe/Dublin"
                }
            event["end"] = {
                    "date": shift.get_end(),
                    "timeZone": "Europe/Dublin"
                }
        else:   
            event["start"] =  {
                "dateTime": shift.get_start(),
                "timeZone": "Europe/Dublin"
            }
            event["end"] = {
                "dateTime": shift.get_end(),
                "timeZone": "Europe/Dublin"
            }

        event = service.events().insert(calendarId=CALENDER_ID, body=event).execute()
        event_ids.append(event["id"])

    print("Your roster has successfully been added to your Google Calendar\n")
    hours = calc_total_hours(shifts)
    print(f"Total hours: {hours}")

    undo = input("Would you like to delete these events? (y/n) ").lower()
    if undo == "y":
        for event_id in event_ids:
            service.events().delete(calendarId=CALENDER_ID, eventId=event_id).execute()     
        
        print("Your roster has been deleted")


def main():
    auth = Auth(SCOPES)
    creds = auth.get_credentials()
    calendar_service = build("calendar", "v3", credentials=creds)
    ocr = OCR()
    ocr.run()
    shifts = read_shifts(FILENAME)
    upload_roster(calendar_service, shifts)

if __name__ == "__main__":
    main()


import argparse
import csv
import datetime
import pyautogui
import time

PYTHON_FOR_BEGINNERS = "Python For Beginners"
GANS_WITH_PYTHON = "GANs with Python"
INTRO_TO_GITHUB = "Introduction to GitHub and Version Control"

MIN_ATTENDANCE = 3
MAX_ATTENDANCE = 0
DAYS_BEFORE_WORKSHOP_OPENS = 7

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4

EVENT_INFO_Y = 518
ADD_EVENT_POS = (2958, 296)
EVENT_DATE_POS = (3364, EVENT_INFO_Y)
DONE_BUTTON_POS = (4403, 914)
START_TIME_POS = (3656, EVENT_INFO_Y)
FINISH_TIME_POS = (4007, EVENT_INFO_Y)
APPROX_TIME_POS = (4330, EVENT_INFO_Y)
MIN_ATTEND_POS = (5009, EVENT_INFO_Y)
MAX_ATTENT_POS = (5371, EVENT_INFO_Y)
NOTES_POS = (2931, 739)


parser = argparse.ArgumentParser()
parser.add_argument(
    "workshop", nargs="?", default=PYTHON_FOR_BEGINNERS
)  # change when this is finished
args = parser.parse_args()


def _get_ordinal_day(day: str) -> str:
    """Get the ordinal format of a day.

    Args:
        day (str): The day of the month in DD form.

    Returns:
        str: Day of the month with ordinal suffix.
    """
    day = int(day)
    if day >= 4 and day <= 20:
        return str(day) + "th"
    if day % 10 == 1:
        return str(day) + "st"
    if day % 10 == 2:
        return str(day) + "nd"
    if day % 10 == 3:
        return str(day) + "rd"
    return str(day) + "th"


def _create_registration_message(date: str) -> str:
    """Creates a message about when a workshop will open.

    Args:
        date (str): The date of the workshop in the form DD/MM/YYY.

    Returns:
        str: A string saying registration for the workshop will open a week before its start date.
    """
    date = datetime.datetime.strptime(date, "%d/%m/%Y") - datetime.timedelta(
        days=DAYS_BEFORE_WORKSHOP_OPENS
    )
    day_name = date.strftime("%A")
    ordinal_day_of_month = _get_ordinal_day(date.strftime("%d"))
    month_name = date.strftime("%B")
    return f"Registration will open on {day_name} {ordinal_day_of_month} {month_name}."

def add_event():
    """Clicks the Add Event button.
    """
    pyautogui.click(*ADD_EVENT_POS)

def set_event_info(pos: tuple, input: str):
    """Enters some information in the ORB workshop event fields.

    Args:
        pos (tuple): A tuple of the mouse position for the field.
        input (str): A string of information to be entered in the field.
    """
    pyautogui.click(*pos)
    time.sleep(1)
    pyautogui.write(input)

print("15 seconds to make sure your mouse is in the right place...")
time.sleep(15)

with open("workshops.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    for row in workshops:
        if len(row) > 0 and row[0].lower() == args.workshop.lower():
            add_event()
            set_event_info(EVENT_DATE_POS, row[DATE_IDX])
            # Press the done button after giving date
            pyautogui.click(*DONE_BUTTON_POS)
            time.sleep(1)
            set_event_info(START_TIME_POS, row[START_TIME_IDX])
            set_event_info(FINISH_TIME_POS, row[END_TIME_IDX])
            set_event_info(MIN_ATTEND_POS, str(MIN_ATTENDANCE))
            set_event_info(MAX_ATTENT_POS, str(MAX_ATTENDANCE))
            set_event_info(NOTES_POS, "test test " + _create_registration_message(row[DATE_IDX]))


import argparse
import csv
import datetime
import time

import pyautogui

PYTHON_FOR_BEGINNERS = "Python For Beginners"
GANS_WITH_PYTHON = "GANs with Python"
INTRO_TO_GITHUB = "Introduction to GitHub and Version Control"

WORKSHOP_NAMES = {
    PYTHON_FOR_BEGINNERS: "2 - Python",
    GANS_WITH_PYTHON: "2 - GANs",
    INTRO_TO_GITHUB: "2 - GitHub",
}

MAX_ATTENDANCE = 1
WEEKS_BEFORE_WORKSHOP_OPENS = 1

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4
DATE_STRING_LENGTH = len("DD/MM/YYYY")

parser = argparse.ArgumentParser()
parser.add_argument("workshop")
parser.add_argument(
    "cutoff", nargs="?", default=datetime.datetime.today().strftime("%d/%m/%Y")
)
args = parser.parse_args()

CUT_OFF_DATE = datetime.datetime.strptime(args.cutoff, "%d/%m/%Y")

CALENDAR_WORKSHOP_NAME = WORKSHOP_NAMES[args.workshop]


def _get_ordinal_day(day: str) -> str:
    """Get the ordinal format of a day.

    Args:
        day (str): The day of the month in DD form.

    Returns:
        str: Day of the month with ordinal suffix.
    """
    day = int(day)
    if 4 <= day <= 20:
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
        date (str): The date of the workshop in the form DD/MM/YYYY.

    Returns:
        str: A string saying registration for the workshop will open a week before its start date.
    """
    print(date)
    date = datetime.datetime.strptime(date, "%d/%m/%Y") - datetime.timedelta(
        weeks=WEEKS_BEFORE_WORKSHOP_OPENS
    )
    day_name = date.strftime("%A")
    ordinal_day_of_month = _get_ordinal_day(date.strftime("%d"))
    month_name = date.strftime("%B")
    return f"Registration will open on {day_name} {ordinal_day_of_month} {month_name}."


def before_cut_off_date(workshop_date: str) -> bool:
    """Checks if the workshop date is before or on the cut off date.

    Args:
        workshop_date (str): The date of the workshop.

    Returns:
        bool: True if the workshop is on or before the cut off date, False otherwise.
    """
    return datetime.datetime.strptime(workshop_date, "%d/%m/%Y") <= CUT_OFF_DATE


def write_to_text_field():
    pyautogui.write("LCC")


def press_tab(count: int):
    for _ in range(count):
        pyautogui.press("tab")


def set_event_times(date: str):
    date = datetime.datetime.strptime(date, "%d/%m/%Y")


# DELAY = 5
# print(f"{str(DELAY)} seconds to make sure your mouse is in the right place...")
# time.sleep(DELAY)

with open("calendar.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    workshops = [
        row
        for row in reversed(list(workshops))
        if len(row) > 0
        and row[0] == CALENDAR_WORKSHOP_NAME
        and not before_cut_off_date(row[DATE_IDX])
    ]

print(workshops)

# press_tab(10)
# write_to_text_field("LCC")
# press_tab(2)
# write_to_text_field("WG28B")
# press_tab(2)
#
# pyautogui.press("down")
# press_tab(1)

# set_event_times(row[DATE_IDX])
# pyautogui.press("enter")
# set_event_info(NOTES_POS, _create_registration_message(row[DATE_IDX]))
# pyautogui.scroll(600)

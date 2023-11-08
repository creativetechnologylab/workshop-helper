import argparse
import csv
import datetime
import time

import pyautogui

PYTHON_FOR_BEGINNERS = "Python For Beginners"
GANS_WITH_PYTHON = "GANs with Python"
INTRO_TO_GITHUB = "Intro to GitHub and Version Control"

MIN_ATTENDANCE = 3
MAX_ATTENDANCE = 0
WEEKS_BEFORE_WORKSHOP_OPENS = 1

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4
DATE_STRING_LENGTH = len("DD/MM/YYYY")

EVENT_INFO_Y = 535
ADD_EVENT_POS = (2988, 301)
DONE_BUTTON_POS = (4409, 936)
HEADING_POS = (2935, 416)
DATE_INPUT_POS = (4432, 852)
EVENT_DATE_POS = (3335, EVENT_INFO_Y)
START_TIME_POS = (3672, EVENT_INFO_Y)
FINISH_TIME_POS = (3956, EVENT_INFO_Y)
APPROX_TIME_POS = (4331, EVENT_INFO_Y)
MIN_ATTEND_POS = (5021, EVENT_INFO_Y)
MAX_ATTENT_POS = (5365, EVENT_INFO_Y)
NOTES_POS = (2987, 748)


parser = argparse.ArgumentParser()
parser.add_argument("workshop")
parser.add_argument(
    "cutoff", args="?", default=datetime.datetime.today().strftime("%d/%m/%Y")
)
args = parser.parse_args()

CUT_OFF_DATE = datetime.datetime.strptime(args.cutoff, "%d/%m/%Y")


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


def add_event():
    """Clicks the Add Event button."""
    pyautogui.click(*ADD_EVENT_POS)
    time.sleep(2)


def set_event_info(pos: tuple, input: str):
    """Enters some information in the ORB workshop event fields.

    Args:
        pos (tuple): A tuple of the mouse position for the field.
        input (str): A string of information to be entered in the field.
    """
    pyautogui.click(*pos)
    time.sleep(1)
    pyautogui.write(input)


def set_event_date(date: str):
    """Enters the event date.

    Args:
        date (str): The date of the workshop in a DD/MM/YYY format.
    """
    pyautogui.click(*EVENT_DATE_POS)
    pyautogui.click(*DATE_INPUT_POS, clicks=2, interval=1)
    for _ in range(DATE_STRING_LENGTH):
        pyautogui.press("backspace")
    pyautogui.write(date)
    time.sleep(1)
    pyautogui.click(*DONE_BUTTON_POS)
    time.sleep(2)
    print(date)


def before_cut_off_date(workshop_date: str) -> bool:
    """Checks if the workshop date is before or on the cut off date.

    Args:
        workshop_date (str): The date of the workshop.

    Returns:
        bool: True if the workshop is on or before the cut off date, False otherwise.
    """
    return datetime.datetime.strptime(workshop_date, "%d/%m/%Y") <= CUT_OFF_DATE


def set_event_times(position: tuple, time: str):
    """Sets the time info for the workshop.

    Args:
        position (tuple): The position of the event start/end time field.
        time (str): The time that should be inputted.
    """
    set_event_info(position, time)
    pyautogui.press("enter")
    pyautogui.press("down")
    pyautogui.press("enter")


DELAY = 5
print(f"{str(DELAY)} seconds to make sure your mouse is in the right place...")
time.sleep(DELAY)

with open("workshops.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    for row in reversed(list(workshops)):
        if len(row) > 0 and row[0].lower() == args.workshop.lower():
            if before_cut_off_date(row[DATE_IDX]):
                continue
            add_event()
            set_event_date(row[DATE_IDX])
            set_event_times(START_TIME_POS, row[START_TIME_IDX][:-3])
            set_event_times(FINISH_TIME_POS, row[END_TIME_IDX][:-3])
            set_event_info(MIN_ATTEND_POS, str(MIN_ATTENDANCE))
            set_event_info(MAX_ATTENT_POS, str(MAX_ATTENDANCE))
            set_event_info(HEADING_POS, row[0] + " in WG28B")
            set_event_info(NOTES_POS, _create_registration_message(row[DATE_IDX]))
            pyautogui.scroll(600)

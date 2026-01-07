import argparse
import csv
import datetime
import time

import pyautogui

HOME = "home"
DOWN = "down"
CTRL = "ctrl"
ENTER = "enter"

PYTHON_FOR_BEGINNERS = "python"
GEN_AI_WITH_PYTHON = "gen-ai"
INTRO_TO_GITHUB = "github"

WORKSHOP_NAMES = {
    PYTHON_FOR_BEGINNERS: "2 - Python For Beginners",
    GEN_AI_WITH_PYTHON: "2 - Generative AI with Python",
    INTRO_TO_GITHUB: "2 - Introduction to GitHub and Version Control",
}

FULL_NAME = {
    "2 - Python For Beginners": "Python For Beginners",
    "2 - Generative AI with Python": "Generative AI with Python",
    "2 - Introduction to GitHub and Version Control": "Introduction to GitHub and Version Control",
}

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4
WEEKS_BEFORE_WORKSHOP_OPENS = 1

parser = argparse.ArgumentParser()
parser.add_argument("--workshop", nargs="?", default=None)
parser.add_argument(
    "--cutoff", nargs="?", default=datetime.datetime.today().strftime("%d/%m/%Y")
)
args = parser.parse_args()

CUT_OFF_DATE = datetime.datetime.strptime(args.cutoff, "%d/%m/%Y")

if args.workshop is not None:
    CALENDAR_WORKSHOP_NAME = WORKSHOP_NAMES[args.workshop]
else:
    CALENDAR_WORKSHOP_NAME = None


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


def press_tab(count: int):
    """Repeatedly presses the tab key to move around the page.

    Args:
        count: Number of times the tab button should be pressed.

    """
    pyautogui.press("tab", presses=count, interval=0.1)


def _set_date(date):
    """Enters the date information for the workshop.

    Args:
        date: The date object.

    """
    press_tab(1)
    pyautogui.press(HOME)
    for _ in range(date.month - 1):
        pyautogui.press(DOWN)

    pyautogui.keyDown("shift")
    press_tab(1)
    pyautogui.keyUp("shift")
    pyautogui.press(HOME)
    for _ in range(date.day - 1):
        pyautogui.press(DOWN)
    press_tab(1)


def _enter_time_information(session_time):
    """Enters the start and end times for the workshop.

    Args:
        session_time: The time object.

    """
    pyautogui.press(HOME)
    for _ in range(session_time.hour):
        pyautogui.press(DOWN)
    press_tab(1)

    pyautogui.press(HOME)
    for _ in range(session_time.minute):
        pyautogui.press(DOWN)


def set_event_times(date: str, start_time: str, end_time: str):
    """
    Sets the event date and time information for the workshop.
    Args:
        date: The workshop date.
        start_time: The workshop start time.
        end_time:  The workshop end time.

    """
    date = datetime.datetime.strptime(date, "%d/%m/%Y")
    start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
    end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

    _set_date(date)
    press_tab(2)

    _enter_time_information(start_time)

    press_tab(2)
    _set_date(date)
    press_tab(2)

    _enter_time_information(end_time)


if CALENDAR_WORKSHOP_NAME:
    DELAY = 5
    print(f"{str(DELAY)} seconds to make sure your mouse is in the right place...")
    time.sleep(DELAY)

    with open("workshops.csv", "r") as workshops_file:
        workshops = csv.reader(workshops_file, delimiter=",")
        workshops = [
            row
            for row in reversed(list(workshops))
            if len(row) > 0
            and row[0] == CALENDAR_WORKSHOP_NAME
            and not before_cut_off_date(row[DATE_IDX])
        ]

    for ws in workshops:

        # look for "add new session" link
        pyautogui.keyDown(CTRL)
        pyautogui.press("f")
        pyautogui.keyUp(CTRL)
        pyautogui.write("Add")
        pyautogui.press(ENTER)

        # open the link - this only works with chromium
        pyautogui.keyDown(CTRL)
        pyautogui.press(ENTER)
        pyautogui.keyUp(CTRL)

        # wait for new page to load
        time.sleep(5)

        # enter location and room information
        press_tab(6)
        pyautogui.write("LCC")
        press_tab(2)
        pyautogui.write("WG28B")
        press_tab(2)
        pyautogui.press(DOWN)

        # set the event time/date information
        press_tab(1)
        set_event_times(ws[DATE_IDX], ws[START_TIME_IDX], ws[END_TIME_IDX])

        # give session capacity as 1 to start with
        press_tab(7)
        pyautogui.write("1")

        # don't allow overbooking for now
        press_tab(11)

        # create the workshop
        pyautogui.press(ENTER)
        time.sleep(10)

else:
    with open("workshops.csv", "r") as workshops_file:
        rows = csv.reader(workshops_file, delimiter=",")

        workshops = []
        for row in reversed(list(rows)):

            if (
                len(row) > 0
                and row[0] in WORKSHOP_NAMES.values()
                and not before_cut_off_date(row[DATE_IDX])
            ):
                row[0] = FULL_NAME[row[0]]
                row[DATE_IDX] = datetime.datetime.strptime(row[DATE_IDX], "%d/%m/%Y")
                workshops.append(row)

        workshops = sorted(workshops, key=lambda x: x[DATE_IDX])

        # 07/11 – 15:00 – 16:30 - Workshop name
        for ws in workshops:
            print(
                f"{ws[DATE_IDX].strftime('%d/%m')} - {ws[START_TIME_IDX][:-3]} - {ws[END_TIME_IDX][:-3]} - {ws[0]}"
            )

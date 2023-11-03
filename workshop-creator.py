import csv
import argparse
import datetime

PYTHON_FOR_BEGINNERS = "python for beginners"
GANS_WITH_PYTHON = "gans with python"
INTRO_TO_GITHUB = "introduction to github and version control"

MIN_ATTENDANCE = 3
MAX_ATTENDANCE = 0
DAYS_BEFORE_WORKSHOP_OPENS = 7

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4

parser = argparse.ArgumentParser()
parser.add_argument(
    "workshop", nargs="?", default=PYTHON_FOR_BEGINNERS
)  # change when this is finished
args = parser.parse_args()


def _get_ordinal_day(day):
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
    if day % 10 == 3:
        return str(day) + "rd"
    if day % 10 == 2:
        return str(day) + "nd"
    return str(day) + "th"


def _create_registration_message(date):
    """Creates a message about when a workshop will open.

    Args:
        date (str): The date of the workshop in the form DD/MM/YYY

    Returns:
        str: A string saying registration for the workshop will open a week before its start date.
    """
    date = datetime.datetime.strptime(date, "%d/%m/%Y") - datetime.timedelta(
        days=DAYS_BEFORE_WORKSHOP_OPENS
    )
    day_name = date.strftime("%A")
    ordinal_day_of_month = _get_ordinal_day(date.strftime("%d"))
    month = date.strftime("%B")
    return f"Registration will open on {day_name} {ordinal_day_of_month} {month}."


with open("workshops.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    for row in workshops:
        if len(row) > 0 and row[0].lower() == args.workshop:
            # print(row[DATE_IDX], row[START_TIME_IDX], row[END_TIME_IDX])
            print(_create_registration_message(row[DATE_IDX]))

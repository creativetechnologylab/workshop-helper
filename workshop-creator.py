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
# parser.add_argument("workshop")
parser.parse_args()


def _create_registration_message(date):
    date = datetime.datetime.strptime(date, "%d/%m/%Y") - datetime.timedelta(
        days=DAYS_BEFORE_WORKSHOP_OPENS
    )
    date = date.strftime("%A %d %B")
    return f"Registration will open on {date}."


with open("workshops.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    for row in workshops:
        if len(row) > 0 and row[0] == "Python For Beginners":
            # print(row[DATE_IDX], row[START_TIME_IDX], row[END_TIME_IDX])
            print(_create_registration_message(row[DATE_IDX]))

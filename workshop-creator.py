import csv
import argparse

parser = argparse.ArgumentParser()
parser.parse_args()

PYTHON_FOR_BEGINNERS = "python for beginners"
GANS_WITH_PYTHON = "gans with python"
INTRO_TO_GITHUB = "introduction to github and version control"

MIN_ATTENDANCE = 3
MAX_ATTENDANCE = 0

DATE_IDX = 1
START_TIME_IDX = 2
END_TIME_IDX = 4

def _create_registration_message(date):
    return "Registration will open on"

with open("workshops.csv", "r") as workshops_file:
    workshops = csv.reader(workshops_file, delimiter=",")
    for row in workshops:
        if len(row) > 0 and row[0] == "Python For Beginners":
            print(row[DATE_IDX], row[START_TIME_IDX], row[END_TIME_IDX])
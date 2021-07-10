import argparse
import os
from datetime import date, datetime, time, timedelta
from random import randint
from uuid import uuid1 as uuid

from git import Repo
from git.exc import InvalidGitRepositoryError


def random_time():
    return time(randint(0, 23), randint(0, 59), randint(0, 59), randint(0, 999999))


def date_list(days):
    today = date.today()
    dates = []
    for day in range(days):
        d = today - timedelta(days=day)
        # no. commits on a single day can range from 1 to 7
        for _ in range(randint(1, 7)):
            dates.append(datetime.combine(d, random_time()))
    return dates


def make_commits(days):
    for d in date_list(days):
        date_iso = d.strftime("%Y-%m-%d %H:%M:%S")
        with open(FILENAME, "w") as file:
            file.write(CODE)
        repo.index.add([FILENAME])
        # all thanks to stackoverflow for next two lines...
        os.environ["GIT_AUTHOR_DATE"] = date_iso
        os.environ["GIT_COMMITTER_DATE"] = date_iso
        # commit changes with random id as commit message
        repo.index.commit(str(uuid()))


def init():

    global repo
    try:
        repo = Repo(os.getcwd())  # for existing repo
    except InvalidGitRepositoryError:  # if there is no existing repo
        repo = Repo.init(os.getcwd())  # initialize new repo

    assert not repo.bare, "Unable to Initialize Repository"
    return repo


if __name__ == "__main__":
    # total number of days
    FILENAME = "helloworld.py"
    CODE = "print('Hello World')"

    parser = argparse.ArgumentParser(description="Create fake commits in Past")

    parser.add_argument(
        "-d", "--days", metavar="days", type=int, help="Total number of days for commit"
    )
    args = parser.parse_args()

    init()

    num_days = args.days
    if num_days is None:
        num_days = 1

    make_commits(num_days)

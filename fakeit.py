import os
from git import Repo
from git.exc import InvalidGitRepositoryError
from datetime import time, date, timedelta, datetime
from random import randint
from uuid import uuid1 as uuid

FILENAME = "helloworld.py"
CODE = "print('Hello World')"

try:
    repo = Repo(os.getcwd())
    assert not repo.bare
except InvalidGitRepositoryError:
    repo = Repo.init(os.getcwd())
    assert not repo.bare

def random_time():
    return time(randint(0, 23), randint(0, 59), randint(0, 59), randint(0, 999999))

def date_list(days):
    today = date.today()
    dates = []
    for day in range(days):
        d = today - timedelta(days=day)
        for i in range(randint(1, 10)):
            dates.append(datetime.combine(d, random_time()))
    return dates

def make_commits(days):
    for d in date_list(days):
        date_iso = d.strftime("%Y-%m-%d %H:%M:%S")
        with open(FILENAME, 'w') as file:
            file.write(CODE)
        repo.index.add([FILENAME])
        os.environ['GIT_AUTHOR_DATE'] = date_iso
        os.environ['GIT_COMMITTER_DATE'] = date_iso
        repo.index.commit(str(uuid()))

if __name__ == "__main__":
    make_commits(5)

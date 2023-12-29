#!/usr/bin/env python3

import sys
import csv
import requests


def get_tacs():
    """
    Get tacs from SamloaderKotlin and build a dict mapping models to list of
    possible tacs
    """
    req = requests.get('https://raw.githubusercontent.com/zacharee/SamloaderKotlin/master/common/src/commonMain/resources/MR/files/tacs.csv')

    if req.status_code != 200:
        print("Could not fetch tacs.csv")
        return 1

    c = csv.reader(req.content.decode('utf8').split('\n'))

    # skip header
    next(c)

    tacs = {}
    for row in c:
        if len(row) < 2:
            continue
        tacs.setdefault(row[1], []).append(row[0])
        if len(row) < 3:
            continue
        tacs.setdefault(row[2], []).append(row[0])

    with open('samloader/tacs.py', 'w', encoding='utf8') as tacs_py:
        print('# Generated with get_tacs.py in parent directory\n',
              file=tacs_py)
        print('TACS =', tacs, file=tacs_py)

    return 0


if __name__ == '__main__':
    sys.exit(get_tacs())

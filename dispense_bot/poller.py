# -*- coding: utf-8 -*-
# vim: set ai et ts=4 sts=4 sw=4 syntax=python:

from __future__ import print_function

import logging
import os
import pprint
import re
import requests
import sys

from dispense_bot import dispense as _dispense

_HOOK_ADDRESS = os.getenv("RECEIVER_ADDR", "127.0.0.1:5000")
_MM_PATTERN = re.compile(r"[mM]\s?(&|'[nN]'|[aA][nN][dD]?)?\s?[mM]'?[sS]?")
_NUTS_PATTERN = re.compile(r"([nN][uU][tT][sSzZ]*|[aA][lL][mM][oO][nN][dD][sSzZ]*|[tT][rR][aA][iI][lL]*)")


def parse(resp):
    text = resp.get("text", "")
    subj = resp.get("subj", "")
    req = subj.lower() + text.lower()

    if len(_MM_PATTERN.findall(req)) > 0:
        return 1

    if len(_NUTS_PATTERN.findall(req)) > 0:
        return 2

    return 0


def dispense(dispenser_no):
    if dispenser_no not in _dispense.VALID_CHANNELS:
        return
    print("\nDispensing from:", dispenser_no)
    _dispense.dispense_to(dispenser_no)


def run():
    print("Start!")

    _dispense.init()

    address = "http://{addr}/mailgun/read".format(addr=_HOOK_ADDRESS)

    while True:
        try:
            r = requests.get(address)
            resp = r.json()
            if resp:
                dispenser_no = parse(resp)
                dispense(dispenser_no)

            sys.stdout.write(".")
            sys.stdout.flush()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=True)
    run()

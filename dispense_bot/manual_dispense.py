#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set ai et ts=4 sts=4 sw=4 syntax=python:

import logging
import sys

from dispense_bot import dispense as _dispense

DISPENSE_TURNS = 2
VALID_CHANNELS = [1, 2]

motor_channel = 1
try:
    motor_channel = int(sys.argv[1])
except IndexError:
    print("defaulting to motor 1 for dispensing")
    pass

if motor_channel not in VALID_CHANNELS:
    raise ValueError("Invalid motor channel: {}, expected one of: {}".format(
        motor_channel,
        VALID_CHANNELS,
    ))


def run():
    _dispense.init()
    _dispense.dispense_to(motor_channel)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=True)
    run(motor_channel)

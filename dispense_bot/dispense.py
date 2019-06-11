#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set ai et ts=4 sts=4 sw=4 syntax=python:

import atexit
import logging
import sys
import time
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime, timedelta

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

_log = logging.getLogger(__name__)
_mh = None
_last_dispensed_time = None

DEFAULT_SPR = 200  # Default Steps-per-Revolution
DEFAULT_RPM = 30  # Default Revolutions-per-Minute
DISPENSE_COOLDOWN = timedelta(seconds=30)
VALID_CHANNELS = [1, 2]
CHANNEL_MOTOR_MAP = {
    1: [1, 2],
    2: [3, 4],
}
DISPENSER_SERVE_STRATEGY = {
    # RIGHT
    #1: [
    #      OrderedDict([
    #          (Adafruit_MotorHAT.FORWARD, 50),
    #          (Adafruit_MotorHAT.BACKWARD, 25),
    #      ]),
    #      OrderedDict([
    #          (Adafruit_MotorHAT.BACKWARD, 50),
    #          (Adafruit_MotorHAT.FORWARD, 75),
    #      ]),
    #],
    1: [
        OrderedDict([
            (Adafruit_MotorHAT.FORWARD, 66),
            (Adafruit_MotorHAT.BACKWARD, 50),
        ]),
    ],
    # LEFT
    2: [
          OrderedDict([
              (Adafruit_MotorHAT.FORWARD, 100),
              (Adafruit_MotorHAT.BACKWARD, 50),
          ]),
          OrderedDict([
              (Adafruit_MotorHAT.BACKWARD, 125),
              (Adafruit_MotorHAT.FORWARD, 50),
          ]),
    ],
}


def init(hat_config=None):

    global _mh

    # create a default object, no changes to I2C address or frequency
    if hat_config is None:
        hat_config = {}

    _mh = Adafruit_MotorHAT(**hat_config)

    # recommended for auto-disabling motors on shutdown!
    atexit.register(turn_off_motors)


def turn_off_motors():
    """ Release all of the motors
    """

    global _mh

    _log.info("Shutting down all motors")

    for i in range(1, 5):
        _mh.getMotor(i).run(Adafruit_MotorHAT.RELEASE)


def can_dispense():
    """ Figure out if snacks can be dispensed
    """

    global _last_dispensed_time

#     if _last_dispensed_time is None:
#         return True
# 
#     if (_last_dispensed_time + DISPENSE_COOLDOWN) < datetime.utcnow():
#         return True

    return True


@contextmanager
def using_stepper(channel, steps_per_rev=DEFAULT_SPR, rpm=DEFAULT_RPM):

    global _mh

    # initialize the stepper
    _log.info("Create stepper controller: {} (spr={}, rpm={})".format(
        channel,
        steps_per_rev,
        rpm,
    ))
    stepper = _mh.getStepper(steps_per_rev, channel)
    stepper.setSpeed(rpm)

    # pass the stepper up to the parent context
    yield stepper

    # release the stepper
    _log.info("Releasing stepper: {}".format(channel))
    motor_nums = CHANNEL_MOTOR_MAP[channel]
    for motor in motor_nums:
        _mh.getMotor(motor).run(Adafruit_MotorHAT.RELEASE)


def dispense_to(motor_channel):

    if motor_channel not in VALID_CHANNELS:
        raise ValueError("Invalid motor channel: {}, expected one of: {}".format(
            motor_channel,
            VALID_CHANNELS,
        ))

    if not can_dispense():
        raise RuntimeError("Dispenser cooldown period - {}".format(str(DISPENSE_COOLDOWN)))

    with using_stepper(motor_channel) as stepper:
        # Get the dispense rates
        dispenser_strategy = DISPENSER_SERVE_STRATEGY[motor_channel]
        for operations in dispenser_strategy:
            _log.info("Executing operation set: {}".format(operations))

            for direction, steps in operations.items():
                stepper.step(steps, direction,  Adafruit_MotorHAT.DOUBLE)

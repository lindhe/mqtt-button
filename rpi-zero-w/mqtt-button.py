#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

""" A simple program that sends an MQTT messsage upon GPIO button press. """

import argparse
import sys
from datetime import datetime as dt
from signal import pause

import paho.mqtt.publish as pub
from gpiozero import Button
from gpiozero.pins.mock import MockFactory

__version__ = '1.0.0'


def main(topic: str, pressed_msg: str, released_msg: str, hostname: str,
         gpio_pin: int, mocked: bool, inverted: bool):
    """ GPIO initialization and registering signal event handlers. """
    pin_factory = MockFactory() if mocked else None
    button = Button(gpio_pin, pin_factory=pin_factory)
    if inverted:
        pressed_msg, released_msg = released_msg, pressed_msg

    def pressed_handler():
        event(topic=topic, event=pressed_msg, hostname=hostname)

    def released_handler():
        event(topic=topic, event=released_msg, hostname=hostname)

    button.when_pressed = pressed_handler
    button.when_released = released_handler

    print("Button is ready!")
    pause()


def event(topic="/", event="PRESSED", hostname="localhost"):
    """ Broadcasts an event. """
    print(f"Registered {event.lower()} at {str(dt.now())}")
    pub.single(topic, payload=event.upper(), hostname=hostname)


if __name__ == '__main__':
    # Bootstrapping
    p = argparse.ArgumentParser(description="Sends an MQTT message upon button"
                                + " press")
    # Add cli arguments
    p.add_argument('-H', '--hostname', help="Hostname to MQTT server",
                   default="localhost")
    p.add_argument('-g', '--gpio-pin', help="GPIO pin for the button",
                   type=int, default=24)
    p.add_argument('--inverted', help="Invert button state " +
                   "(default: closed circuit == pressed)",
                   action="store_true")
    p.add_argument('-p', '--pressed-message', default="PRESSED",
                   help="Payload for MQTT message when button is pressed")
    p.add_argument('-r', '--released-message', default="RELEASED",
                   help="Payload for MQTT message when button is released")
    p.add_argument('--mocked',
                   help="Use keyboard input instead of GPIO button",
                   action="store_true")
    p.add_argument('-t', '--topic', help="MQTT topic to publish to",
                   default="/")
    p.add_argument('--version', action='version', version=__version__)
    # Run:
    args = p.parse_args()
    try:
        main(
            topic=args.topic,
            pressed_msg=args.pressed_message,
            released_msg=args.released_message,
            hostname=args.hostname,
            gpio_pin=args.gpio_pin,
            mocked=args.mocked,
            inverted=args.inverted
        )
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by ^C\n")

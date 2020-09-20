#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

""" A simple program that sends an MQTT messsage upon GPIO button press. """

import sys
import argparse
import paho.mqtt.publish as pub
import time
from gpiozero.pins.mock import MockFactory
from gpiozero import Button


def main(topic: str, message: str, hostname: str, gpio_pin: int, mocked: bool,
         inverted: bool, interval: int):
    """ GPIO initialization and main loop. """
    if mocked:
        button = Button(gpio_pin, pin_factory=MockFactory())
    else:
        button = Button(gpio_pin)
    while True:
        if mocked:
            input("Please press Enter...")
        else:
            if inverted:
                button.wait_for_release()
            else:
                button.wait_for_press()
        print("The button was pressed!")
        pub.single(topic, payload=message, hostname=hostname)
        time.sleep(interval)


if __name__ == '__main__':
    # Bootstrapping
    p = argparse.ArgumentParser(description="Sends an MQTT message upon button"
                                + " press")
    # Add cli arguments
    p.add_argument('-H', '--hostname', help="Hostname to MQTT server",
                   default="localhost")
    p.add_argument('-g', '--gpio-pin', help="GPIO pin for the button",
                   type=int, default=17)
    p.add_argument('-i', '--interval', help="Interval with which to check" +
                   " button state", type=int, default=30)
    p.add_argument('--inverted', help="Invert button state " +
                   "(default: closed circuit == pressed)",
                   action="store_true")
    p.add_argument('-m', '--message', help="Payload for MQTT message",
                   default="")
    p.add_argument('--mocked',
                   help="Use keyboard input instead of GPIO button",
                   action="store_true")
    p.add_argument('-t', '--topic', help="MQTT topic to publish to",
                   default="/")
    # Run:
    args = p.parse_args()
    try:
        main(
            topic=args.topic,
            message=args.message,
            hostname=args.hostname,
            gpio_pin=args.gpio_pin,
            mocked=args.mocked,
            inverted=args.inverted,
            interval=args.interval
        )
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by ^C\n")

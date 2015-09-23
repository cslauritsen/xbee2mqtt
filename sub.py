#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 syntax=on

#   Xbee to MQTT gateway
#   Copyright (C) 2012-2013 by Xose Pérez
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__app__ = "Xbee to MQTT gateway"
__version__ = "0.4.20130708"
__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2012-2013 Xose Pérez"
__license__ = 'GPL v3'

import os
import sys
import time

#from tests.SerialMock import Serial
from libs.config import Config
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
        """
        Message received from a subscribed topic
        """
        print "Message received"
        print("%s %s %s" % (time.asctime(), msg.topic, msg.payload))


if __name__ == "__main__":

    def resolve_path(path):
        return path if path[0] == '/' else os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

    config_file = resolve_path('config/xbee2mqtt.yaml');
    config = Config(config_file)

    host = config.get('mqtt', 'host', 'localhost')
    port = config.get('mqtt', 'port', 1883)
    username = config.get('mqtt', 'username', None)
    password = config.get('mqtt', 'password', None)

    client = mqtt.Client()
    client.on_message = on_message
    if username:
      client.username_pw_set(username, password)
    client.connect(host, port, 60)

    client.subscribe('#', qos=0)

    while True:
        try:
            client.loop()
        except Exception as e:
            print("Error while looping MQTT (%s)" % e)


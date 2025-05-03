#!/usr/bin/env python3

import os
import json
import traceback
import sys
from flask import Flask
from flask import request
from wiim_device import WiimDevice

wiim_ip_addr = str(sys.argv[1])

if wiim_ip_addr is None:
    print("You must pass the im device ip address in argument arg1")
    exit(1)

wiim_device = WiimDevice(wiim_ip_addr, verbose=False)
app = Flask(__name__)

# process the standard Wiim API
@app.route('/httpapi.asp')
def command_compat():
    command = request.args.get("command", "")
    if command is None:
        return "no command specified", 404
    return wiim_device.run_command(command)

@app.route("/command/<path:command>")
def run_command(command):
    return wiim_device.run_command(command)

# media commands

@app.route("/media/play")
def media_play():
    wiim_device.media_play()
    return "OK"

@app.route("/media/pause")
def media_pause():
    wiim_device.media_pause()
    return "OK"

@app.route("/media/toggle")
def media_toggle():
    wiim_device.media_toggle()
    return "OK"

@app.route("/media/prev")
def media_prev():
    wiim_device.media_prev()
    return "OK"

@app.route("/media/next")
def media_next():
    wiim_device.media_next()
    return "OK"

# volume control commands

@app.route("/vol/up", defaults={"amount": 2})
@app.route("/vol/up/<int:amount>")
def volume_up(amount):
    wiim_device.volume_up(amount)
    return "OK"

@app.route("/vol/down", defaults={"amount": 2})
@app.route("/vol/down/<int:amount>")
def volume_down(amount):
    wiim_device.volume_down(amount)
    return "OK"

@app.route("/vol/<int:volume>")
def volume_set(volume):
    wiim_device.set_volume(volume)
    return "OK"

# volume mute commands

@app.route("/mute/on")
def media_mute():
    wiim_device.mute()
    return "OK"

@app.route("/mute/off")
def media_unmute():
    wiim_device.unmute()
    return "OK"

@app.route("/mute/toggle")
def media_mute_toggle():
    wiim_device.toggle_mute()
    return "OK"

# change input commands

@app.route("/input/line-in")
def media_input_line():
    wiim_device.set_line_in()
    return "OK"

@app.route("/input/wifi")
def media_input_wifi():
    wiim_device.set_wifi_in()
    return "OK"

@app.route("/input/hdmi")
def media_input_hdmi():
    wiim_device.set_hdmi_in()
    return "OK"

@app.route("/input/optical")
def media_input_optical():
    wiim_device.set_optical_in()
    return "OK"

@app.route("/input/phono")
def media_input_phono():
    wiim_device.set_phono_in()
    return "OK"

@app.route("/input/bluetooth")
def media_input_bluetooth():
    wiim_device.set_bluetooth_in()
    return "OK"

# change output commands

@app.route("/output/optical")
def media_output_optical():
    wiim_device.set_opt_out()
    return "OK"

@app.route("/output/line-out")
def media_output_line():
    wiim_device.set_line_out()
    return "OK"

@app.route("/output/coax")
def media_output_coax():
    wiim_device.set_coax_out()
    return "OK"

@app.route("/output/headphone")
def media_output_headphone():
    wiim_device.set_headphone_out()
    return "OK"

@app.route("/output/bluetooth")
def media_output_bluetooth():
    wiim_device.set_bluetooth_out()
    return "OK"

@app.route("/output/dlna")
def media_output_dlna():
    wiim_device.set_dlna_out()
    return "OK"

# run a preset

@app.route("/preset/<int:pre_numb>")
def preset_set(pre_numb):
    wiim_device.preset(pre_numb)
    return "OK"

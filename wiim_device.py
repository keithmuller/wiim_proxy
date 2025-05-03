#!/usr/bin/env python3

import requests
import json
import urllib3

urllib3.disable_warnings()

class WiimDevice:
    def __init__(self, ip, verbose=0):
        self.ip = ip
        self.verbose = verbose

    def run_command(self, command):
        url = "https://%s/httpapi.asp?command=%s" % (self.ip, command)
        response = requests.get(url, verify=False)
        if self.verbose == 1:
            print("API command: {0}".format(command))
        if self.verbose == 2:
            print("API command: {0}, got {1}".format(command, response.text))
        return response.text

    def get_player_status(self):
        text = self.run_command("getPlayerStatus")
        data = json.loads(text)
        return data

    # Change input

    def set_line_in(self):
        self.run_command("setPlayerCmd:switchmode:line-in")

    def set_optical_in(self):
        self.run_command("setPlayerCmd:switchmode:optical")

    def set_wifi_in(self):
        self.run_command("setPlayerCmd:switchmode:wifi")

    def set_hdmi_in(self):
        self.run_command("setPlayerCmd:switchmode:HDMI")

    def set_phono_in(self):
        self.run_command("setPlayerCmd:switchmode:phono")

    def set_bluetooth_in(self):
        self.run_command("setPlayerCmd:switchmode:bluetooth")

    def media_play_url(self, url):
        self.run_command("setPlayerCmd:play:{0}".format(url))

    # Change output

    def set_opt_out(self):
        self.run_command("setAudioOutputHardwareMode:1")

    def set_line_out(self):
        self.run_command("setAudioOutputHardwareMode:2")

    def set_coax_out(self):
        self.run_command("setAudioOutputHardwareMode:3")

    def set_headphone_out(self):
        self.run_command("setAudioOutputHardwareMode:4")

    def set_bluetooth_out(self):
        self.run_command("setAudioOutputHardwareMode:5")

    def set_dlna_out(self):
        self.run_command("setAudioOutputHardwareMode:6")

    # Media controls

    def media_play(self):
        self.run_command("setPlayerCmd:play")

    def media_pause(self):
        self.run_command("setPlayerCmd:pause")

    def media_toggle(self):
        self.run_command("setPlayerCmd:onepause")

    def media_prev(self):
        self.run_command("setPlayerCmd:prev")

    def media_next(self):
        self.run_command("setPlayerCmd:next")

    # Volume up and down

    def get_volume(self, status=None):
        if status is None:
            status = self.get_player_status()
        return status["vol"]

    def set_volume(self, volume):
        volume = int(volume)
        volume = max(0,min(100,volume))
        self.run_command("setPlayerCmd:vol:{0}".format(volume))

    def volume_up(self, step):
        volume = int(self.get_volume())
        self.set_volume(volume + step)

    def volume_down(self, step):
        volume = int(self.get_volume())
        self.set_volume(volume - step)

    # Mute the volume

    def mute(self):
        self.run_command("setPlayerCmd:mute:0")

    def unmute(self):
        self.run_command("setPlayerCmd:mute:1")

    def toggle_mute(self, status=None):
        if status is None:
            status = self.get_player_status()
        muted = status["mute"] == "0"
        if (muted):
            self.unmute()
        else:
            self.mute()

    # Run a Preset

    def preset(self, pre_numb):
        pre_numb = int(pre_numb)
        pre_numb = max(1,min(12,pre_numb))
        self.run_command("MCUKeyShortClick:{0}".format(pre_numb))

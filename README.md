***THIS MAY NOT WORK WITH YOUR WIIM IF ITS NOT A WIIM ULTRA***

This is a http proxy server that provide a http only control interface
to a wiim device.

An example is adding a sofabaton x1s wifi virtual device to control a wiim
device.

This server uses uwsgi and is intended for use only on internal networks
that are safely behind a firewall.

This package uses systemd to start wiim_proxy at boot.

This server was tested using raspios (bookworm) 64-bit on a pi4 and pi5

This server supports all the controls (except power) found on the wiim remote.
It uses the published wiim http(s) interface to communicate with the wiim device

# How to Install wiim_proxy http server on a system (raspios bookworm)

(1) Examine and maybe edit the file Makefile. Pay attention to the settings
    at the top of the file. You should not need to change DESTDIR SYSMD OWNER
    GROUP. Do not change FILES.

(2) Edit wiim_proxy.ini
    (a) Change the ip address (10.0.1.103) in the line "pyargv=10.0.1.103"
        to the ip address of the wiim device you want to control
    (b) Run the follow to make sure the port number is not being used:
         netstat -a | grep 5050
        This should have no return string.
    (c) If you got a return like:
	tcp   0   0 0.0.0.0:5050    0.0.0.0:*       LISTEN  
        Change the port number (5050) in the line "http-socket = :5050"
        to a port that is not used

(3) This package is set to be installed in /opt/wiim_proxy and run as user
    and group www-data
    If you want to change this, you will need to adjust the setting in
    the files wiim_proxy.service and Makefile to be consistent.

(4) After completing steps (1) and (2) (make sure you can sudo first)
    Copy the files to /opt/wiim_proxy:
    make install

(5) Now install the required packages:
    make pkg_install

(6) We use systemd to start the wiim_proxy server at boot 
    (a) Create a symbolic link
       /etc/systemd/system/wiim_proxy.service
       that points at
       /opt/wiim_proxy/wiim_proxy.service and enable the wiim_proxy server
       and then enable wiim_proxy as a service.
       To do this:
       make service_install
    (b) wiim_proxy will start at reboot. Only if you want to start it now 
        before a reboot:
        make service_start
    (c) After you have started wiim_proxy, running:
        netstat -a | grep 5050
        should return a line that looks like:
	tcp   0   0 0.0.0.0:5050    0.0.0.0:*       LISTEN  

(7) Do a reboot and try step (7c) above to make sure all is well

(8) Test the proxy server.
    As an example, assume the ip where wiim_proxy is running is 10.0.1.153
    The port number is 5050. The ip address of the wiim device is 10.0.1.103

    From any web browser (or use curl) connect to:
        http://10.0.1.153:5050/input/line-in
    You should get:
        ok
    in the browser.

# list of commands

In the following list <ip> is the name or ip address of the system where this
server is running and <port> is its port number ("http-socket = :5050")

http://$ip:$port/media/play
http://$ip:$port/media/pause
http://$ip:$port/media/toggle
http://$ip:$port/media/prev
http://$ip:$port/media/next

    (<int> below must be between 0 and 100)
http://$ip:$port/volume/up
http://$ip:$port/volume/up/<int>
http://$ip:$port/volume/down
http://$ip:$port/volume/down/<int>
http://$ip:$port/volume/<int>

http://$ip:$port/mute/on
http://$ip:$port/mute/off
http://$ip:$port/mute/toggle

http://$ip:$port/input/line-in
http://$ip:$port/input/wifi 
    (above also works with ethernet conneted wiims)
http://$ip:$port/input/hdmi
http://$ip:$port/input/optical
http://$ip:$port/input/phono
http://$ip:$port/input/bluetooth

http://$ip:$port/output/optical
http://$ip:$port/output/line-out
http://$ip:$port/output/coax
http://$ip:$port/output/headphone
http://$ip:$port/output/bluetooth
http://$ip:$port/output/dlna

http://$ip:$port/preset/<int>

This server is backwards compatible with the published Wiim API.

http://$ip:$port/httpapi.asp?command=$command
http://$ip:$port/command/$command
